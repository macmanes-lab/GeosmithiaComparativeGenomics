#!/usr/bin/perl -w
#
# seqCat.pl v1.0
# Last modified July 29, 2005 13:35
# (c) Olaf R.P. Bininda-Emonds
#
# Input:
#   One or more sequence files in any of fasta, nexus or Se-Al formats
#
# Output:
#   A nexus-formatted file with the different data partitions presented in an
#   interleaved fashion and corrected for any missing taxa.
#
# Usage: seqCat.pl -d<filename> [-i<f|n|p|s>] [-v] [-h]
#	options: -d<filename> = text file containing names of sequence files, one per line
#            -i<f|n|p|s> = format of sequence files (fasta (f -- default), nexus (n), phylip (p) or Se-Al (s))
#            -h = print this message and quit
#            -v = verbose output

use strict;

# Set user-input defaults and associated parameters
	# I/O variables
		my ($nameFile, @fileNames);
		my $outFile = "seqCat_sequences.nex";

		my $inputType = "fasta";	# Options are "fasta", "nexus", , "phylip", and "Se-Al"
		my ($header, $tempAcc, $tempName, $tempSeq, $fastaAcc, $sealCode);
		my $owner = 0;
		my $sealDelFlag = 0;
		my $globalGenCode = 1;

	# Data set variables
		my (@partitionList, %partName, %seqLength);
		my (@accNum, %nameLabel, %sequence, %geneticCode, %accPresent);
		my (@allTaxa, %taxonCount);
		my $seqCount;
		my %seqData;
		my $nchar;

	# Miscellaneous variables
		my $verbose = 0;
		my $debug = 0;

# Process flags
	for (my $i = 0; $i <= $#ARGV; $i++)
		{
		if ($ARGV[$i] =~ /^-d(.*)/)
			{
			$nameFile = $1;
			}
		elsif ($ARGV[$i] eq "-if")
			{
			$inputType = "fasta";
			}
		elsif ($ARGV[$i] eq "-in")
			{
			$inputType = "nexus";
			}
		elsif ($ARGV[$i] eq "-ip")
			{
			$inputType = "phylip";
			}
		elsif ($ARGV[$i] eq "-is")
			{
			$inputType = "Se-Al";
			}
		elsif ($ARGV[$i] eq "-v")
			{
			$verbose = 1;
			}
		elsif ($ARGV[$i] eq "-x")
			{
			$verbose = $debug = 1;
			}
		elsif ($ARGV[$i] eq "-h")
			{
			print "Usage: seqCat.pl -d<filename> [-i<f|n|p|s>] [-v] [-h]\n";
			print "Options: -d<filename> = text file containing names of sequence files, one per line\n";
			print "         -i<f|n|p|s> = format of sequence files (fasta (f -- default), nexus (n), phylip (p) or Se-Al (s))\n";
			print "         -h = print this message and quit\n";
			print "         -v = verbose output\n";
			exit(0);
			}
		else
			{
			print "Don't understand argument: $ARGV[$i]\n";
			print "Usage: seqCat.pl -d<filename> [-i<f|n|p|s>] [-v] [-h]\n";
			exit(1); 
			}
		}

die "ERROR: Must supply name of text file containing names of sequence files.\n" if (not $nameFile);
	
# Read in names of sequence files
	setLineBreak($nameFile);
	open (FILES, "<$nameFile") or die "Cannot open file containing names of sequence files, $nameFile\n";
		while (<FILES>)
			{
			chomp;
			next unless ($_);
			$_ =~ s/^\s+//;
			$_ =~ s/\s+$//;
			push @fileNames, $_;
			(my $partitionName = $_) =~ s/\.\w+$//;
			push @partitionList, $partitionName;
				$partName{$_} = $partitionName;
			}

# Read in sequence data
	foreach my $seqFile (@fileNames)
		{
		my $nexusRead = 0;
		undef @accNum;
		
		seqRead($seqFile);

		# Process individual sequences for partition
			$seqLength{$partName{$seqFile}} = 0;
			foreach my $accession (@accNum)
				{
				$seqData{$nameLabel{$accession}}{$partName{$seqFile}} = $sequence{$accession};
				$seqLength{$partName{$seqFile}} = length($sequence{$accession}) if (length($sequence{$accession}) > $seqLength{$partName{$seqFile}});
				$taxonCount{$nameLabel{$accession}}++;
					push @allTaxa, $nameLabel{$accession} if ($taxonCount{$nameLabel{$accession}} == 1);
				}
			$nchar += $seqLength{$partName{$seqFile}};
			
		if ($verbose)
			{
			print "\tPartition name: $partName{$seqFile}\n";
			printf "\tNumber of sequences: %s\n", scalar(@accNum);
			print "\tMaximal sequence length: $seqLength{$partName{$seqFile}}\n";
			printf "\tConcatentated data set: $nchar bps for %s species\n", scalar(@allTaxa);
			}
		}

# Print results!
	print "\nPrinting results to nexus-formatted file $outFile...\n";
	
	@allTaxa = sort (@allTaxa);
	@partitionList = sort (@partitionList);

	open (NEX, ">$outFile") or die "Cannot open nexus file for aligned DNA sequences, $outFile";
		print NEX "#nexus\n\n";
		print NEX "begin data;\n";
		printf NEX "\tdimensions ntax = %s nchar = $nchar;\n", scalar(@allTaxa);
		print NEX "\tformat  datatype = DNA interleave=yes gap = - missing = ?;\n\n";
		print NEX "\tmatrix\n\n";
		
		foreach my $partition (@partitionList)
			{
			my $blankSeq = "?" x $seqLength{$partition};
			print NEX "[Source of sequence data: $partition]\n\n";
			foreach my $taxon (@allTaxa)
				{
				if (defined $seqData{$taxon}{$partition})
					{
					print NEX "\t$taxon\t$seqData{$taxon}{$partition}\n";
					}
				else
					{
					print NEX "\t$taxon\t$blankSeq\n";
					} 
				}
			}

		print NEX "\t;\nend;\n\n";
		
		my $charsetStart = 1;
		print NEX "begin paup;\n";
		foreach my $partition (@partitionList)
			{
			print NEX "\tcharset $partition = ";
			if ($seqLength{$partition} == 1)
				{
				print NEX "$charsetStart;\n";
				$charsetStart++;
				}
			else
				{
				printf NEX "$charsetStart - %s;\n", $charsetStart + $seqLength{$partition} - 1;
				$charsetStart += $seqLength{$partition};
				}
			}
		print NEX "end;\n";
			
	close NEX;

exit(0);

### Subroutines used in the program

sub seqRead
	{
	my $seqFile = shift;

	print "\nReading in sequence data from file $seqFile (type is $inputType) ...\n" if ($inputType);
	setLineBreak($seqFile);
	open (SEQ, "<$seqFile") or die "Cannot open file containing sequences, $seqFile\n";
		my ($header, $tempAcc, $tempName, $tempSeq);
		my $fastaAcc;
		my (%nexusSpecies, %nexusAcc, $nexusRead);
		my ($phylipLineCount, $phylipTaxa, $phylipChars, %phylipSeq);
		my $sealCode;
		my ($sealDelFlag, $owner) = (0, 0);

		while (<SEQ>)
			{
			chomp;
			my $lineRead = $_;
			next unless ($lineRead);
			
			# Autodetect sequence format
				if (not $inputType)
					{
					$inputType = "fasta" if ($lineRead =~ /^>/);
					$inputType = "nexus" if ($lineRead =~ /\#nexus/i);
					$inputType = "phylip" if ($lineRead =~ /^\s*\d+\s+\d+/);
					$inputType = "Se-Al" if ($lineRead =~ /^\s*Database=\{/i);
					print "\nReading in sequence data from file $seqFile (type determined to be $inputType) ...\n" if ($inputType);
					}
			
			if ($inputType eq "nexus")
				{
				# Only read in data lines
					if ($lineRead =~ /^\s*matrix/i)
						{
						$nexusRead = 1;
						next;
						}
					$nexusRead = 0 if ($lineRead =~ /;\s*$/);
					next unless ($nexusRead);
					next unless ($lineRead =~ /a/i or $lineRead =~ /c/i or $lineRead =~ /g/i or $lineRead =~ /t/i);
				# Clean up input line
					$lineRead =~ s/^\s+//;
					$lineRead =~ s/\'//g;
				my ($species, $seq) = split(/\s+/, $lineRead);
					$species =~ s/\s+/_/g;
				if (not defined $nexusSpecies{$species})
					{
					$nexusSpecies{$species} = 1;
					$seqCount++;
					$nexusAcc{$species} = "tAlign_".$seqCount;
					push @accNum, $nexusAcc{$species};
						$nameLabel{$nexusAcc{$species}} = $species;
						$sequence{$nexusAcc{$species}} = uc($seq);
						$geneticCode{$nexusAcc{$species}} = $globalGenCode;
					}
				else	# Sequences are in interleaved format; append sequence
					{
					$sequence{$nexusAcc{$species}} .= uc($seq);
					}
				}

			if ($inputType eq "fasta")
				{
				if ($lineRead =~/^\s*>/)
					{
					my $species;
					$seqCount++;
					(my $tempSpecies = $lineRead) =~ s/^\s*>//;
					
						if ($tempSpecies =~ /^Mit\.\s+/)	# Entry comes from European RNA project
							{
							$tempSpecies =~ s/^Mit\.\s+//i;	# To fix entries from European RNA project
							my @speciesInfo = split(/\s+/, $tempSpecies);
								$species = join('_', $speciesInfo[0], $speciesInfo[1]);
							if (defined $speciesInfo[2])
								{
								$fastaAcc = $speciesInfo[2];
								}
							else
								{
								$fastaAcc = "tAlign_".$seqCount;
								}
							}
						else
							{
							my @speciesLine = split(/\s+/, $tempSpecies);
							if ($speciesLine[$#speciesLine] =~ /^\(?[A-Z]+\d+\)?$/ and scalar(@speciesLine) > 1)	# Check whether last entry is an accession number
								{
								$fastaAcc = pop (@speciesLine);
								$fastaAcc =~ s/^\(//g;
								$fastaAcc =~ s/\)$//g;
								}
							else
								{
								$fastaAcc = "tAlign_".$seqCount;
								}
							$species = join('_', @speciesLine);
								$species = "Sequence_".$seqCount if ($species eq "");
							}
					push @accNum, $fastaAcc;
						$geneticCode{$fastaAcc} = $globalGenCode;
					$nameLabel{$fastaAcc} = $species;
					}
				else
					{
					$sequence{$fastaAcc} .= uc($lineRead);
					}
				}

			if ($inputType eq "Se-Al")
				{
				my $header;
				$sealDelFlag = 1 if ($lineRead =~/MCoL/);	# Se-Al sometimes places deleted species at end of file; do not read in remainder of file
					next if ($sealDelFlag == 1);
				next unless ($lineRead =~/NumSites/i or $lineRead =~/Owner/i or $lineRead =~/Name/i or $lineRead =~/Accession/i or $lineRead =~/Sequence/i or $lineRead =~/GeneticCode/i);
				if ($lineRead =~/Owner\s*\=\s*(\d+)/i)
					{
					$owner = $1;
					}
				if ($lineRead =~/Accession/i and $owner == 2)
					{
					$seqCount++;
					if ($lineRead =~ /null/ or $lineRead =~ /\"\"/)
						{
						$tempAcc = "tAlign_".$seqCount;
						}
					else
						{
						($header, $tempAcc) = split (/=/, $lineRead);
							$tempAcc =~ s/\"//g;
							$tempAcc =~ s/;//g;
						}
					push @accNum, $tempAcc;
					}
				if ($lineRead =~/Name/i and $owner == 2)
					{
					($header, $tempName) = split (/=/, $lineRead);
						$tempName =~ s/\"//g;
						$tempName =~ s/\s*;//g;
					}
				if ($lineRead =~/GeneticCode/i and $owner == 2)
					{
					($header, $sealCode) = split (/=/, $lineRead);
						$sealCode =~ s/\"//g;
						$sealCode =~ s/\s*;//g;
						$geneticCode{$tempAcc} = $sealCode + 1;
					}
				if ($lineRead =~/Sequence/i and $owner == 2)
					{
					($header, $tempSeq) = split (/=/, $lineRead);
						$tempSeq =~ s/\"//g;
						$tempSeq =~ s/;//g;
					$nameLabel{$tempAcc} = $tempName;
					$sequence{$tempAcc} = uc($tempSeq);
					}
				}

			if ($inputType eq "phylip")
				{
				if ($lineRead =~ /^\s*(\d+)\s+(\d+)/)
					{
					$phylipTaxa = $1;
					$phylipChars = $2;
					$phylipLineCount = 0;
					}
				else
					{
					$phylipLineCount++;
					
					$lineRead =~ s/\s//g;
					
					$phylipSeq{$phylipLineCount} .= $lineRead;
					
					$phylipLineCount = 0 if ($phylipLineCount == $phylipTaxa);
					}
				}
			}
	close SEQ;
	
	if ($inputType eq "phylip")	# Postprocess input to derive taxon names and sequence; accounts for both sequential and extended formatting
		{
		for (my $i = 1; $i <= $phylipTaxa; $i++)
			{
			my $phylipAcc = "tAlign_" . $i;
			
			push @accNum, $phylipAcc;
			$geneticCode{$phylipAcc} = $globalGenCode;
			
			# Derive taxon name and sequence
				$sequence{$phylipAcc} = uc(substr($phylipSeq{$i}, 0 - $phylipChars));
				$nameLabel{$phylipAcc} = substr($phylipSeq{$i}, 0, length($phylipSeq{$i}) - $phylipChars);
					$nameLabel{$phylipAcc} =~ s/\s+//g;
			}
		}
	}

sub setLineBreak	# Check line breaks of input files and set input record separator accordingly
	{
	my $inFile = shift;
	$/ ="\n";
	open (IN, "<$inFile") or die "Cannot open $inFile to check form of line breaks.\n";
		while (<IN>)
			{
			if ($_ =~ /\r\n/)
				{
				print "\tDOS line breaks detected ...\n" if ($verbose);
				$/ ="\r\n";
				last;
				}
			elsif ($_ =~ /\r/)
				{
				print "\tMac line breaks detected ...\n" if ($verbose);
				$/ ="\r";
				last;
				}
			else
				{
				print "\tUnix line breaks detected ...\n" if ($verbose);
				$/ ="\n";
				last;
				}
			}
	close IN;
	}

# Version history
#
#	v1.0 (July 29, 2005)
#		- initial release
