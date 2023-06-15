import shutil
import os
# Source directory to copy from(comment or uncomment to change src)
# src_dir = '/home/jose/jyutping-translation/format data/inputs/inputs(jyut+char)'
# src_dir = '/home/jose/jyutping-translation/format data/inputs/inputs(jyut_only)'
src_dir = '/home/jose/jyutping-translation/format data/inputs/inputs(homeland jyut+char)'
# src_dir = '/format data/inputs/inputs(homeland jyut_only)'


# Destination directory to copy to
# dest_dir = '/home/jose/neural_chinese_transliterator/neural_chinese_transliterator/inputs(jyut+char)'
# dest_dir = '/home/jose/neural_chinese_transliterator/neural_chinese_transliterator/inputs(jyut_only)'
dest_dir = '/home/jose/neural_chinese_transliterator/neural_chinese_transliterator/inputs(homeland jyut+char)'
# dest_dir = '/home/jose/neural_chinese_transliterator/neural_chinese_transliterator/inputs(homeland jyut_only)'

if not os.path.exists(dest_dir):
    os.makedirs(dest_dir)

# Use shutil.rmtree to recursively delete the directory and all of its contents
shutil.rmtree(dest_dir)
# Use shutil.copytree to recursively copy the source directory to the destination
shutil.copytree(src_dir, dest_dir)
