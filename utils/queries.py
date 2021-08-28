save_dna_query = "INSERT INTO dna (dna,type,count) VALUES (%s,%s,%s);"
get_dna_query = "SELECT * FROM dna WHERE dna=%s;"
update_dna_query = "UPDATE dna SET count=count+1 WHERE dna=%s;"

stats_query = "SELECT SUM(CASE WHEN type = 'M' THEN count ELSE 0 END) count_mutant_dna, SUM(CASE WHEN type = 'H' THEN count ELSE 0 END) count_human_dna from dna;"
