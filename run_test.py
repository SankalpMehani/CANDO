import sys, os
import cando as cnd
print(os.path.dirname(cnd.__file__))
cnd.get_test()
os.chdir("test")
print('\n')

# Set all variables
matrix_file = 'test-matrix.tsv'
inds_map = 'test-inds.tsv'
cmpd_map = 'test-cmpds.tsv'
cmpd_dir = 'test-cmpds_pdb/'
cmpd_scores = 'test-cmpd_scores.tsv'
prot_scores = 'test-prot_scores.tsv'
pwp = 'test-pathway-prot.tsv'
pwm = 'test-pathway-mesh.tsv'
ncpus = 3

print("Test #1 - generate a toy matrix")
print('-------')
cnd.generate_matrix(matrix_file=matrix_file, cmpd_scores=cmpd_scores, prot_scores=prot_scores, ncpus=ncpus)
print('\n')

print("Test #2 - create CANDO object and run canbenchmark test")
print('-------')
cando = cnd.CANDO(cmpd_map, inds_map, matrix=matrix_file, compute_distance=True,
                  save_dists='test_rmsds.tsv', ncpus=ncpus)
cando.canbenchmark('test')
print('\n')

print("Test #3 - create CANDO object using cosine distance metric then run continuous, bottom, cluster, "
      "and associated benchmark test with 'sort' ranking")
print('-------')
cando_cos = cnd.CANDO(cmpd_map, inds_map, matrix=matrix_file, compute_distance=True, dist_metric='cosine', ncpus=ncpus)
cando_cos.canbenchmark('test_continuous', continuous=True, ranking='ordinal')
cando_cos.canbenchmark_associated('test_associated', ranking='modified')
cando_cos.canbenchmark_bottom('test_bottom', ranking='standard')
cando_cos.canbenchmark_bottom('test_bottom', ranking='modified')
cando_cos.canbenchmark_bottom('test_bottom', ranking='ordinal')
cando_cos.canbenchmark_cluster(n_clusters=5)
print('\n')

print("Test #4 - canpredict_compounds()")
print("\tpredict top10 compounds for Breast Cancer")
print('-------')
cando.canpredict_compounds("MESH:D001943", n=10, topX=10)
cando.canpredict_compounds("MESH:D001943", n=10, topX=25, keep_associated=True)
print('\n')

print("Test #5 - generate fingerprint, scores, and interaction signature for three old compounds and one new compound")
print('-------')
cnd.generate_scores(fp="ob_fp4", cmpd_pdb="8100.pdb", out_path=".")
cnd.generate_scores(fp="rd_ecfp4", cmpd_pdb="8100.pdb", out_path=".")
cnd.generate_signature(cmpd_scores="rd_ecfp4/8100_scores.tsv", prot_scores=prot_scores)
print('\n')

print("Test #6 - Most similar compounds to new compound and CANDO compound signatures")
print('-------')
cando.add_cmpd("8100_signature.tsv", "scy-635")
tc = cando.get_compound(64)
cando.similar_compounds(tc, n=10)
cando.similar_compounds(cando.compounds[10], n=10)
print('\n')

print("Test #7 - canpredict_indications() for new compound and CANDO compound signatures")
print('-------')
cando.canpredict_indications(tc, n=10)
cando.canpredict_indications(cando.compounds[10], n=10)
print('\n')

print("Test #8 - use customized protein set with 20 UniProt IDs, use benchmark with SVM ML code")
print('-------')
cando_uni = cnd.CANDO(cmpd_map, inds_map, matrix=matrix_file, compute_distance=True, protein_set="test-uniprot_set")
cando_uni.ml(benchmark=True, method='rf', seed=50, out='test_svm')
print('\n')

print("Test #9 - use random forest ML code to make predictions for Inflammation for two compounds")
print('-------')
cando_rf = cnd.CANDO(cmpd_map, inds_map, compute_distance=True, matrix=matrix_file)
inflm = cando_rf.get_indication('MESH:D007249')
lys = cando_rf.get_compound(18)
men = cando_rf.get_compound(62)
cando_rf.ml(effect=inflm, predict=[lys, men], method='rf')
print('\n')

print("Test #10 - read .fpt matrices, convert_to_tsv, then fuse with 'mult'")
print('-------')
cnd.Matrix("toy64x.fpt", convert_to_tsv=True)
cnd.Matrix("vina64x.fpt", convert_to_tsv=True)
toy64 = cnd.CANDO(cmpd_map, inds_map, matrix='toy64x.tsv', compute_distance=True, save_dists='toy64x_rmsds.tsv')
vina64 = cnd.CANDO(cmpd_map, inds_map, matrix='vina64x.tsv', compute_distance=True)
vina64.normalize()
print(vina64)
v2rmsd = cnd.CANDO(cmpd_map, inds_map, read_dists='test_rmsds.tsv')
fus_mult = toy64.fusion([vina64], method='mult')
fus_sum = v2rmsd.fusion([vina64], method='sum')
tr = cnd.Matrix('toy64x_rmsds.tsv', dist=True)
tr.convert('toy64x_sim.tsv')
print('\n')

'''
print("Test #11 - Check other download functions")
print('-------')
cnd.get_tutorial()
cnd.get_v2()
print('\n')
'''

print("Test #12 - Pathways data plus benchmark")
print('-------')
cpw = cnd.CANDO(cmpd_map, inds_map, matrix=matrix_file, pathways=pwp, pathway_quantifier='max', compute_distance=True)
cpw.canbenchmark('test-pw')
cpwi = cnd.CANDO(cmpd_map, inds_map, matrix=matrix_file, pathways=pwp, pathway_quantifier='proteins',
                 indication_pathways=pwm)
cpwi.canbenchmark('test-pw_inds')

print("Test #13 - canpredict_denovo() with breast cancer + all proteins and subset of proteins")
print('-------')
cando.canpredict_denovo(method='count', threshold=0.2, ind_id="MESH:D001943", topX=10, save='test-cpdn.tsv')
cando.canpredict_denovo(method='sum', threshold=0.2, topX=10, proteins=['3kzqA', '3w19D', '3lrvA', '2jzjA', '2ys2A'])

print("Test #14 - Search for objects")
print('-------')
cando.search_indication('breast neoplasms')
cando.search_compound('bivlarudn')  # intended typo
cando.get_protein('3kzqA')


