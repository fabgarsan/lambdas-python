save_dna_query = "INSERT INTO dna (dna,type,count) VALUES ('{dna}','{type}',{count});"
get_dna_query = "SELECT * FROM dna WHERE dna='{dna}';"
update_dna_query = "UPDATE dna SET count=count+1 WHERE dna='{dna}';"

stats_query = "SELECT SUM(CASE WHEN type = 'M' THEN count ELSE 0 END) count_mutant_dna, SUM(CASE WHEN type = 'H' THEN count ELSE 0 END) count_human_dna from dna;"
