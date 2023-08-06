#!/usr/bin/env python3


# Classes providing interfaces with annotation databases and the reference genome
#######################################################################################################################

import os
import sys

from cava.utils import core, conseq, csn

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/pysamdir')
import pysam


#######################################################################################################################

# Class representing the Ensembl (transcript) dataset ( can be any database)
class Ensembl(object):
    # Constructor
    def __init__(self, options, genelist, transcriptlist, codon_usage):
        self.options = options
        # Openning tabix file representing the Ensembl database
        self.tabixfile = pysam.Tabixfile(options.args['ensembl'])
        self.proteinSeqs = dict()
        self.exonSeqs = dict()
        self.genelist = genelist
        self.transcriptlist = transcriptlist
        self.codon_usage = codon_usage
        # Transcript to Protein Map for HGVSp protein
        # copy it over to "self" in order to maintain the calling function signature of Record.annotate() called by run() (main.py)
        self.transcript2protein = options.transcript2protein

    # Find transcripts overlapping with a variant
    def findTranscripts(self, variant):
        ret = dict()
        retOUT = dict()

        # Checking chromosome name
        goodchrom = variant.chrom
        if not goodchrom in self.tabixfile.contigs:
            goodchrom = 'chr' + goodchrom
            if not goodchrom in self.tabixfile.contigs: return ret, retOUT

        # Defining variant end points
        if not variant.isInsertion():
            start = variant.pos
            end = variant.pos + len(variant.ref) - 1
        else:
            start = variant.pos - 1
            end = variant.pos

        # Checking both end points of the variant
        reg1 = goodchrom + ':' + str(start) + '-' + str(start)
        reg2 = goodchrom + ':' + str(end) + '-' + str(end)

        if not variant.isSubstitution():
            hits1 = self.tabixfile.fetch(region=reg1)
            hits2 = self.tabixfile.fetch(region=reg2)
            hitdict1 = dict()
            hitdict2 = dict()
            for line in hits1:
                transcript = core.Transcript(line)
                if not (transcript.transcriptStart + 1 <= start <= transcript.transcriptEnd): continue
                # if not strand == transcript.strand: continue
                hitdict1[transcript.TRANSCRIPT] = transcript
            for line in hits2:
                transcript = core.Transcript(line)
                if not (transcript.transcriptStart + 1 <= end <= transcript.transcriptEnd): continue
                #  if not strand == transcript.strand: continue
                hitdict2[transcript.TRANSCRIPT] = transcript

            # Find transcripts with which the variant fully or partially overlaps
            # Does not support multi-transcripts wide deletion (only two adjacent ones)
            for key, transcript in hitdict1.items():

                if len(self.genelist) > 0 and transcript.geneSymbol not in self.genelist: continue
                if len(self.transcriptlist) > 0 and transcript.TRANSCRIPT not in self.transcriptlist: continue

                if key in list(hitdict2.keys()):
                    ret[key] = transcript
                else:
                    if not variant.isInsertion(): retOUT[key] = transcript

            if not variant.isInsertion():
                for key, transcript in hitdict2.items():
                    if len(self.genelist) > 0 and transcript.geneSymbol not in self.genelist: continue
                    if len(self.transcriptlist) > 0 and transcript.TRANSCRIPT not in self.transcriptlist: continue

                    if not key in list(hitdict1.keys()):
                        retOUT[key] = transcript

        else:  # Variant is Substitution
            hits1 = self.tabixfile.fetch(region=reg2)
            for line in hits1:
                transcript = core.Transcript(line)

                if len(self.genelist) > 0 and transcript.geneSymbol not in self.genelist: continue
                if len(self.transcriptlist) > 0 and transcript.TRANSCRIPT not in self.transcriptlist: continue

                if not (transcript.transcriptStart + 1 <= end <= transcript.transcriptEnd): continue
                ret[transcript.TRANSCRIPT] = transcript

        return ret, retOUT

    # Check if a is between x and y
    def inrange(self, x, y, a):
        return x <= a <= y or y <= a <= x

    # Parse CSN coordinates
    def getIntronBases(self, x):
        idx = x.find('-')
        if idx < 1:
            idx = x.find('+')
            if idx < 1: return None
            return int(x[idx:])
        return int(x[idx:])

    # Check if variant is duplication overlapping SS boundary
    def isDupOverlappingSSBoundary(self, csn, ssrange=8):

        if '_p' in csn:
            [cpart, _] = csn.split('_p')
        else:
            cpart = csn

        idx = cpart.find('dup')
        if idx == -1: return False

        cpart = cpart[2:idx]

        if '_' in cpart:
            [x, y] = cpart.split('_')
        else:
            x = self.getIntronBases(cpart)
            if x is None: return False
            return x == ssrange or x == -ssrange

        x = self.getIntronBases(x)
        y = self.getIntronBases(y)
        if x is None or y is None: return False

        return self.inrange(x, y, ssrange) or self.inrange(x, y, -ssrange)

    # Correct CLASS annotations for duplications overlapping SS boundary
    def correctClasses(self, csn, class_plus, class_minus):
        if self.isDupOverlappingSSBoundary(csn, ssrange=int(self.options.args['ssrange'])):
            if class_plus == 'SS' and class_minus == 'INT': return 'INT', 'INT'
            if class_plus == 'INT' and class_minus == 'SS': return 'INT', 'INT'
        return class_plus, class_minus

    # Correct SO annotations for duplications overlapping SS boundary
    def correctSOs(self, csn, so_plus, so_minus):
        if self.isDupOverlappingSSBoundary(csn):
            if so_plus == 'intron_variant|splice_region_variant' and so_minus == 'intron_variant': return 'intron_variant', 'intron_variant'
            if so_plus == 'intron_variant' and so_minus == 'intron_variant|splice_region_variant': return 'intron_variant', 'intron_variant'
        return so_plus, so_minus

    # Annotating a variant based on Ensembl data
    def annotate(self, variant, reference, impactdir):

        # Create left-aligned and right-aligned versions of the variant
        if not variant.isSubstitution():
            variant_plus = variant.alignOnPlusStrand(reference)
            variant_minus = variant.alignOnMinusStrand(reference)
        else:
            variant_plus = variant
            variant_minus = variant

        # Checking if variant alignment makes any difference
        if variant_plus.pos == variant_minus.pos:
            difference = False
        else:
            difference = True

        # Initializing annotation strings
        TRANSCRIPTstring = ''
        GENEstring = ''
        GENEIDstring = ''
        LOCstring = ''
        CSNstring = ''
        CLASSstring = ''
        ALTFLAGstring = ''
        TRINFOstring = ''
        ALTANNstring = ''
        ALTCLASSstring = ''
        SOstring = ''
        ALTSOstring = ''
        IMPACTstring = ''
        PROTPOSstring = ''
        PROTREFstring = ''
        PROTALTstring = ''

        # Collecting transcripts that overlap with the variant
        transcripts_plus, transcriptsOUT_plus = self.findTranscripts(variant_plus)
        transcripts_minus, transcriptsOUT_minus = self.findTranscripts(variant_minus)

        transcripts = set(list(transcripts_plus.keys()) + list(transcripts_minus.keys()))
        transcriptsOUT = set(list(transcriptsOUT_plus.keys()) + list(transcriptsOUT_minus.keys()))

        transcripts = sorted(list(transcripts))
        transcriptsOUT = sorted(list(transcriptsOUT))

        # Annotating with transcripts that only partially overlap with the variant
        for TRANSCRIPT in transcriptsOUT:

            if TRANSCRIPT in transcripts: continue

            if TRANSCRIPT in list(transcriptsOUT_plus.keys()):
                transcript = transcriptsOUT_plus[TRANSCRIPT]
            else:
                transcript = transcriptsOUT_minus[TRANSCRIPT]

            if len(TRANSCRIPTstring) > 0:
                TRANSCRIPTstring += ':'
                GENEstring += ':'
                GENEIDstring += ':'
                TRINFOstring += ':'
                LOCstring += ':'
                CSNstring += ':'
                CLASSstring += ':'
                ALTFLAGstring += ':'
                ALTANNstring += ':'
                ALTCLASSstring += ':'
                SOstring += ':'
                ALTSOstring += ':'
                IMPACTstring += ':'
                PROTPOSstring += ':'
                PROTREFstring += ':'
                PROTALTstring += ':'

            TRANSCRIPTstring += TRANSCRIPT
            GENEstring += transcript.geneSymbol
            GENEIDstring += transcript.geneID
            TRINFOstring += transcript.TRINFO

            if transcript.strand == 1:
                if TRANSCRIPT in list(transcriptsOUT_plus.keys()):
                    LOCstring += 'OUT'
                else:
                    LOCstring += '.'
            else:
                if TRANSCRIPT in list(transcriptsOUT_minus.keys()):
                    LOCstring += 'OUT'
                else:
                    LOCstring += '.'

            CSNstring += '.'
            CLASSstring += '.'
            ALTFLAGstring += '.'
            ALTANNstring += '.'
            ALTCLASSstring += '.'
            SOstring += '.'
            ALTSOstring += '.'
            IMPACTstring += '.'
            PROTPOSstring += '.'
            PROTREFstring += '.'
            PROTALTstring += '.'

        # Iterating through the list of transcripts
        for TRANSCRIPT in transcripts:

            if TRANSCRIPT in list(transcripts_plus.keys()):
                transcript = transcripts_plus[TRANSCRIPT]
            else:
                transcript = transcripts_minus[TRANSCRIPT]

            # Separating annotations by different transcripts with colon
            if len(TRANSCRIPTstring) > 0:
                TRANSCRIPTstring += ':'
                GENEstring += ':'
                GENEIDstring += ':'
                TRINFOstring += ':'
                LOCstring += ':'
                CSNstring += ':'
                CLASSstring += ':'
                ALTFLAGstring += ':'
                ALTANNstring += ':'
                ALTCLASSstring += ':'
                SOstring += ':'
                ALTSOstring += ':'
                IMPACTstring += ':'
                PROTPOSstring += ':'
                PROTREFstring += ':'
                PROTALTstring += ':'

            # Creating the TRANSCRIPT, GENE and TRINFO annotations
            TRANSCRIPTstring += TRANSCRIPT
            GENEstring += transcript.geneSymbol
            GENEIDstring += transcript.geneID
            TRINFOstring += transcript.TRINFO

            # Creating the LOC annotation
            if TRANSCRIPT in list(transcripts_plus.keys()):
                loc_plus = transcript.whereIsThisVariant(variant_plus)
            elif TRANSCRIPT in list(transcriptsOUT_plus.keys()):
                loc_plus = 'OUT'
            else:
                loc_plus = '.'

            if difference:
                if TRANSCRIPT in list(transcripts_minus.keys()):
                    loc_minus = transcript.whereIsThisVariant(variant_minus)
                elif TRANSCRIPT in list(transcriptsOUT_minus.keys()):
                    loc_minus = 'OUT'
                else:
                    loc_minus = '.'
            else:
                loc_minus = loc_plus

            # Creating reference and mutated protein sequence
            notexonic_plus = (
                    ('5UTR' in loc_plus) or ('3UTR' in loc_plus) or ('-' in loc_plus) or ('In' in loc_plus) or (
                    loc_plus == 'OUT') or (loc_plus == '.'))
            if difference:
                notexonic_minus = (('5UTR' in loc_minus) or ('3UTR' in loc_minus) or ('-' in loc_minus) or (
                        'In' in loc_minus) or (loc_minus == 'OUT') or (loc_minus == '.'))
            else:
                notexonic_minus = notexonic_plus
            if notexonic_plus and notexonic_minus:
                protein = ''
            else:
                if not transcript.TRANSCRIPT in list(self.proteinSeqs.keys()):
                    protein, exonseqs = transcript.getProteinSequence(reference, None, None, self.codon_usage)

                    if len(self.proteinSeqs) > 5:
                        self.proteinSeqs = dict()
                        self.exonSeqs = dict()

                    self.proteinSeqs[transcript.TRANSCRIPT] = protein
                    self.exonSeqs[transcript.TRANSCRIPT] = exonseqs
                else:
                    protein = self.proteinSeqs[transcript.TRANSCRIPT]
                    exonseqs = self.exonSeqs[transcript.TRANSCRIPT]

            if notexonic_plus:
                mutprotein_plus = ''
            else:
                mutprotein_plus, exonseqs = transcript.getProteinSequence(reference, variant_plus, exonseqs,
                                                                          self.codon_usage)

            if difference:
                if notexonic_minus:
                    mutprotein_minus = ''
                else:
                    mutprotein_minus, exonseqs = transcript.getProteinSequence(reference, variant_minus, exonseqs,
                                                                               self.codon_usage)
            else:
                mutprotein_minus = mutprotein_plus

            # Creating the CSN annotations both for left and right aligned variant
            if TRANSCRIPT in list(transcripts_plus.keys()):
                csn_plus, protchange_plus = csn.getAnnotation(variant_plus, transcript, reference, protein,
                                                              mutprotein_plus)
                csn_plus_str = csn_plus.getAsString()
            else:
                csn_plus_str, protchange_plus = '.', ('.', '.', '.')

            if difference:
                if TRANSCRIPT in list(transcripts_minus.keys()):
                    csn_minus, protchange_minus = csn.getAnnotation(variant_minus, transcript, reference, protein,
                                                                    mutprotein_minus)
                    csn_minus_str = csn_minus.getAsString()
                else:
                    csn_minus_str, protchange_minus = '.', ('.', '.', '.')
            else:
                csn_minus_str, protchange_minus = csn_plus_str, protchange_plus

            # CLASS, SO and IMPACT

            so_plus = ''
            so_minus = ''
            class_plus = ''
            class_minus = ''
            impact_plus = ''
            impact_minus = ''

            if not impactdir is None or self.options.args['ontology'].upper() in ['CLASS', 'BOTH']:

                # Creating the CLASS annotations both for left and right aligned variant
                if TRANSCRIPT in list(transcripts_plus.keys()):
                    class_plus = conseq.getClassAnnotation(variant_plus, transcript, protein, mutprotein_plus, loc_plus,
                                                           int(self.options.args['ssrange']))
                else:
                    class_plus = '.'

                if difference:
                    if TRANSCRIPT in list(transcripts_minus.keys()):
                        class_minus = conseq.getClassAnnotation(variant_minus, transcript, protein, mutprotein_minus,
                                                                loc_minus, int(self.options.args['ssrange']))
                    else:
                        class_minus = '.'
                else:
                    class_minus = class_plus

            # Determining the IMPACT flag
            if not impactdir is None:

                if TRANSCRIPT in list(transcripts_plus.keys()):
                    if class_plus in list(impactdir.keys()):
                        impact_plus = impactdir[class_plus]
                    else:
                        impact_plus = 'None'
                else:
                    impact_plus = '.'

                if TRANSCRIPT in list(transcripts_minus.keys()):
                    if class_minus in list(impactdir.keys()):
                        impact_minus = impactdir[class_minus]
                    else:
                        impact_minus = 'None'
                else:
                    impact_minus = '.'

            if self.options.args['ontology'].upper() in ['SO', 'BOTH']:
                # Creating the SO annotations both for left and right aligned variant

                if TRANSCRIPT in list(transcripts_plus.keys()):
                    so_plus = conseq.getSequenceOntologyAnnotation(variant_plus, transcript, protein, mutprotein_plus,
                                                                   loc_plus)
                else:
                    so_plus = '.'

                if difference:
                    if TRANSCRIPT in list(transcripts_minus.keys()):
                        so_minus = conseq.getSequenceOntologyAnnotation(variant_minus, transcript, protein,
                                                                        mutprotein_minus, loc_minus)
                    else:
                        so_minus = '.'

                else:
                    so_minus = so_plus

            # Deciding which is the correct CSN and CLASS annotation
            if transcript.strand == 1:
                class_plus, class_minus = self.correctClasses(csn_plus_str, class_plus, class_minus)
                so_plus, so_minus = self.correctSOs(csn_plus_str, so_plus, so_minus)
                CSNstring += csn_plus_str
                CLASSstring += class_plus
                ALTANN = csn_minus_str
                altCLASS = class_minus
                SOstring += so_plus
                altSO = so_minus
                LOCstring += loc_plus
                IMPACTstring += impact_plus
                PROTPOSstring += protchange_plus[0]
                PROTREFstring += protchange_plus[1]
                PROTALTstring += protchange_plus[2]
            else:
                class_plus, class_minus = self.correctClasses(csn_minus_str, class_plus, class_minus)
                so_plus, so_minus = self.correctSOs(csn_minus_str, so_plus, so_minus)
                CSNstring += csn_minus_str
                CLASSstring += class_minus
                ALTANN = csn_plus_str
                altCLASS = class_plus
                SOstring += so_minus
                altSO = so_plus
                LOCstring += loc_minus
                IMPACTstring += impact_minus
                PROTPOSstring += protchange_minus[0]
                PROTREFstring += protchange_minus[1]
                PROTALTstring += protchange_minus[2]

            if self.options.args['givealt']:

                # Creating the ALTANN annotation
                if not csn_plus_str == csn_minus_str:
                    ALTANNstring += ALTANN
                else:
                    ALTANNstring += '.'

                # Creating the ALTCLASS annotation
                if not class_plus == class_minus:
                    ALTCLASSstring += altCLASS
                else:
                    ALTCLASSstring += '.'

                # Creating the ALTSO annotations
                if not so_plus == so_minus:
                    ALTSOstring += altSO
                else:
                    ALTSOstring += '.'

            if (not self.options.args['givealt']) or self.options.args['givealtflag']:
                # Creating the ALTFLAG annotation

                if self.options.args['ontology'].upper() == 'CLASS':
                    if not class_plus == class_minus:
                        ALTFLAGstring += 'AnnAndClass'
                    else:
                        if not csn_plus_str == csn_minus_str:
                            ALTFLAGstring += 'AnnNotClass'
                        else:
                            ALTFLAGstring += 'None'

                if self.options.args['ontology'].upper() == 'SO':
                    if not so_plus == so_minus:
                        ALTFLAGstring += 'AnnAndSO'
                    else:
                        if not csn_plus_str == csn_minus_str:
                            ALTFLAGstring += 'AnnNotSO'
                        else:
                            ALTFLAGstring += 'None'

                if self.options.args['ontology'].upper() == 'BOTH':
                    if not class_plus == class_minus:
                        if not so_plus == so_minus:
                            ALTFLAGstring += 'AnnAndClassAndSO'
                        else:
                            ALTFLAGstring += 'AnnAndClassNotSO'
                    else:
                        if csn_plus_str == csn_minus_str:
                            ALTFLAGstring += 'None'
                        else:
                            if not so_plus == so_minus:
                                ALTFLAGstring += 'AnnAndSONotClass'
                            else:
                                ALTFLAGstring += 'AnnNotClassNotSO'

        # Adding annotations to the variant
        variant.addFlag('TRANSCRIPT', TRANSCRIPTstring)
        variant.addFlag('GENE', GENEstring)
        variant.addFlag('GENEID', GENEIDstring)
        variant.addFlag('TRINFO', TRINFOstring)
        variant.addFlag('LOC', LOCstring)
        variant.addFlag('CSN', CSNstring)
        variant.addFlag('PROTPOS', PROTPOSstring)
        variant.addFlag('PROTREF', PROTREFstring)
        variant.addFlag('PROTALT', PROTALTstring)

        if self.options.args['ontology'].upper() in ['CLASS', 'BOTH']: variant.addFlag('CLASS', CLASSstring)
        if self.options.args['ontology'].upper() in ['SO', 'BOTH']: variant.addFlag('SO', SOstring)

        if not impactdir is None: variant.addFlag('IMPACT', IMPACTstring)

        if self.options.args['givealt']:
            variant.addFlag('ALTANN', ALTANNstring)
            if self.options.args['ontology'].upper() in ['CLASS', 'BOTH']: variant.addFlag('ALTCLASS', ALTCLASSstring)
            if self.options.args['ontology'].upper() in ['SO', 'BOTH']: variant.addFlag('ALTSO', ALTSOstring)

        if (not self.options.args['givealt']) or self.options.args['givealtflag']:
            variant.addFlag('ALTFLAG', ALTFLAGstring)

        return variant


#######################################################################################################################


# Class representing the dbSNP dataset
class dbSNP(object):
    # Constructor
    def __init__(self, options):
        # Openning tabix file representing the dbSNP database
        self.tabixfile = pysam.Tabixfile(options.args['dbsnp'])

    # Annotating a variant based on dbSNP data
    def annotate(self, variant):
        # Checking if variant is a SNP at all
        if variant.isSubstitution():
            # Fetching data from dbSNP database
            goodchrom = variant.chrom
            if not goodchrom in self.tabixfile.contigs:
                goodchrom = 'chr' + goodchrom
                if not goodchrom in self.tabixfile.contigs:
                    variant.addFlag('DBSNP', '')
                    return variant
            reg = goodchrom + ':' + str(variant.pos) + '-' + str(variant.pos)
            lines = self.tabixfile.fetch(region=reg)
            for line in lines:
                cols = line.split('\t')
                # Adding DBSNP annotation to the variant
                alts = cols[3].split(',')
                if variant.alt in alts:
                    variant.addFlag('DBSNP', cols[0])
            if not 'DBSNP' in variant.flags: variant.addFlag('DBSNP', '')
        else:
            variant.addFlag('DBSNP', '')
        return variant


#######################################################################################################################

# Class representing the reference genome dataset
class Reference(object):
    # Constructor
    def __init__(self, options):
        # Openning tabix file representing the reference genome
        self.fastafile = pysam.Fastafile(options.args['reference'])

    # Retrieving the sequence of a genomic region
    def getReference(self, chrom, start, end):
        # Checking if chromosome name exists
        goodchrom = chrom
        if not goodchrom in self.fastafile.references:
            goodchrom = 'chr' + chrom
            if not goodchrom in self.fastafile.references:
                if chrom == 'MT':
                    goodchrom = 'chrM'
                    if not goodchrom in self.fastafile.references: return None
                else:
                    return None

            # Fetching data from reference genome
        if end < start: return core.Sequence('')
        if start < 1: start = 1

        if pysam.__version__ in ['0.7.7', '0.7.8', '0.8.0']:
            last = self.fastafile.getReferenceLength(goodchrom)
        else:
            last = self.fastafile.get_reference_length(goodchrom)

        if end > last: end = last

        seq = self.fastafile.fetch(goodchrom, start - 1, end)
        return core.Sequence(seq.upper())

#######################################################################################################################
