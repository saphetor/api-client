# Copyright 2018 Saphetor S.A.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os
import time
import vcf
from collections import OrderedDict
from vcf.parser import _Info
from varsome_api.client import VarSomeAPIClient
from varsome_api.models.variant import AnnotatedVariant

__author__ = "ckopanos"


class VCFAnnotator(VarSomeAPIClient):
    """
    VCFAnnotator will take an input vcf file parse it and produce an annotated vcf file
    """

    def __init__(self, api_key=None,
                 max_variants_per_batch=1000, ref_genome='hg19', get_parameters=None, max_threads=None):
        super().__init__(api_key, max_variants_per_batch)
        self.ref_genome = ref_genome
        self.get_parameters = get_parameters
        self.total_varialts = 0
        self.filtered_out_variants = 0
        self.variants_with_errors = 0
        self.max_threads = max_threads or 1
        if self.max_variants_per_batch > 3000 and self.max_threads > 1:
            self.logger.warning("Having more than 1 thread with more than 3000 variants per batch may not be optimal")

    def _process_request(self, input_batch):
        start = time.time()
        api_results = self.batch_lookup(list(input_batch.keys()), params=self.get_parameters,
                                        ref_genome=self.ref_genome, max_threads=self.max_threads)
        duration = time.time() - start
        self.logger.info('Annotated %s variants in %s' % (len(input_batch), duration))
        self.logger.info('Writing to output vcf file')
        for i, requested_variant in enumerate(input_batch.keys()):
            try:
                results = api_results[i]
                record = input_batch[requested_variant]
                if results:
                    if 'filtered_out' in results:
                        self.logger.info(results['filtered_out'])
                        self.filtered_out_variants += 1
                        continue
                    if 'error' in results:
                        self.logger.error(results['error'])
                        self.variants_with_errors += 1
                        continue
                    if 'variant_id' in results:
                        variant_result = AnnotatedVariant(**results)
                        record = self.annotate_record(record, variant_result)
                        self.vcf_writer.write_record(record)
                    else:
                        self.logger.error(results)
                        self.variants_with_errors += 1
            except Exception as e:
                self.logger.error(e)
                self.variants_with_errors += 1
                pass  # log an exception..

    def annotate_record(self, record, variant_result):
        """
        Method to annotate a record. You should override this with your own implementation
        to include variant result properties you want in your output vcf
        :param record: vcf record object
        :param variant_result: AnnotatedVariant object
        :return: annotated record object
        """
        record.INFO['variant_id'] = variant_result.variant_id
        record.INFO['gene'] = ",".join(variant_result.genes)
        record.INFO['gnomad_exomes_AF'] = variant_result.gnomad_exomes_af
        record.INFO['gnomad_genomes_AF'] = variant_result.gnomad_genomes_af
        record.ALT = variant_result.alt
        record.POS = variant_result.pos
        record.ID = ";".join(variant_result.rs_ids) or "."
        return record

    def add_vcf_header_info(self, vcf_template):
        """
        Adds vcf INFO headers for the annotated values provided
        This is just a base method you need to override in your own implementation
        depending on the annotations added through the annotate_record method
        :param vcf_template: vcf reader object
        :return:
        """
        vcf_template.infos['variant_id'] = _Info('variant_id', 1, 'Integer', 'Saphetor variant identifier', None, None)
        vcf_template.infos['gene'] = _Info('gene', '.', 'String', 'Genes related to this variant', None, None)
        vcf_template.infos['gnomad_exomes_AF'] = _Info('gnomad_exomes_AF', '.', 'Float',
                                                     'GnomAD exomes allele frequency value', None, None)
        vcf_template.infos['gnomad_genomes_AF'] = _Info('gnomad_genomes_AF', '.', 'Float',
                                                      'GnomAD genomes allele frequency value', None, None)

    def annotate(self, input_vcf_file, output_vcf_file=None, template=None, **kwargs):
        """
        :param input_vcf_file: The input vcf file to be annotated
        :param output_vcf_file: The file to write annotations back if none input_vcf_file.annotated.vcf will be
        generated instead
        :param template: An alternate vcf file to use for vcf file headers. If none the input vcf file will
        be used
        :return:
        """
        annotations_start = time.time()
        if not os.path.isfile(input_vcf_file):
            raise FileNotFoundError('%s does not exist' % input_vcf_file)
        if output_vcf_file is None:
            output_vcf_file = "%s.annotated.vcf" % input_vcf_file
        vcf_reader = vcf.Reader(filename=input_vcf_file, strict_whitespace=kwargs.get('strict_whitespace', True))
        vcf_template = vcf_reader if template is None else vcf.Reader(filename=template, strict_whitespace=kwargs.get(
            'strict_whitespace', True))
        self.add_vcf_header_info(vcf_template)
        self.vcf_writer = vcf.Writer(open(output_vcf_file, 'w'), vcf_template)
        input_batch = OrderedDict()
        # this will keep the request queue large enough so that parallel requests will not stop executing
        batch_limit = self.max_variants_per_batch * self.max_threads * 2
        for record in vcf_reader:
            for alt_seq in record.ALT:
                requested_variant = "%s:%s:%s:%s" % (record.CHROM, record.POS, record.REF or "", alt_seq or "")
                input_batch[requested_variant] = record
                self.total_varialts += 1
            if len(input_batch) < batch_limit:
                continue
            self._process_request(input_batch)
            # reset input batch
            input_batch = OrderedDict()
            # we may have some variants remaining if input batch is less than batch size
        if len(input_batch) > 0:
            self._process_request(input_batch)
        self.vcf_writer.close()
        self.logger.info("Annotating %s variants in %s. "
                         "Filtered out %s. "
                         "Errors %s" % (self.total_varialts, time.time() - annotations_start,
                                        self.filtered_out_variants, self.variants_with_errors))
