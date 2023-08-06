import os 
import boto3
import pandas as pd 
from .transpose import transpose_file

def transpose_file(
    file: str, 
    outfile: str, 
    insep: str, 
    outsep: str,
    chunksize: int, 
    save_chunks: bool,
    quiet=bool, 
) -> None:
    """
    Calculates the transpose of a .csv too large to fit in memory 

    Parameters:
    file: Path to input file 
    outfile: Path to output file (transposed input file)
    sep: Separator for .csv, by default is ,
    chunksize: Number of lines per iteration
    quiet: Boolean indicating whether to print progress or not 

    Returns:
    None
    """

    # First, get the number of lines in the file (total number we have to process)
    with open(file) as f:
        lines = len(f.readlines())
    
    if not quiet: print(f'Number of lines to process is {lines}')

    # Get just the outfile name for writing chunks
    outfile_split = outfile.split('/')
    outfile_name = outfile_split[-1][:-4] # takes /path/to/file.csv --> file 

    if len(outfile_split) == 1: # as in there was no /path/to/file.csv, just file.csv
        chunkfolder = f'chunks_{outfile_name}'
    else:
        outfile_path = f"/{os.path.join(*outfile.split('/')[:-1])}"
        chunkfolder = os.path.join(outfile_path, f'chunks_{outfile_name}')

    if not os.path.isdir(chunkfolder):
        if not quiet: print(f'Making chunk folder {chunkfolder = }')
        os.mkdir(chunkfolder)

    num_chunks = lines // chunksize + int(lines % chunksize == 0) # if we have one last small chunk or not 
    if not quiet: print(f'Total number of chunks is {num_chunks}')

    for df, l in zip(pd.read_csv(file, sep=insep, chunksize=chunksize), range(0, num_chunks + 1)):  
        if not quiet: print(f'Working on chunk {l} out of {num_chunks}')
        df = df.T

        if not quiet: print(f'Writing chunk {l} to csv')
        df.to_csv(os.path.join(chunkfolder, f'{outfile_name}_{l}.csv'), sep=outsep, index=False)

    if not quiet: print(f'Combining chunks from {chunkfolder} into {outfile}')
    os.system(
        f"paste -d ',' {chunkfolder}/* > {outfile}"
    )

    if not save_chunks:
        if not quiet: print('Finished combining chunks, deleting chunks.')
        os.system(
            f'rm -rf {chunkfolder}/*'
        )

    if not quiet: print('Done.')

class Transpose:
    def __init__(
        self, 
        file: str, 
        outfile: str, 
        insep: str=',', 
        outsep: str=',',
        chunksize: str=400, 
        save_chunks: bool=False,
        quiet: bool=False,
    ):
        self.file = file 
        self.outfile = outfile
        self.insep = insep 
        self.outsep = outsep
        self.chunksize = chunksize
        self.save_chunks = save_chunks
        self.quiet = quiet

    def compute(self):
        transpose_file(
            file=self.file,
            outfile=self.outfile,
            insep=self.insep,
            outsep=self.outsep,
            chunksize=self.chunksize,
            save_chunks=self.save_chunks,
            quiet=self.quiet,
        )
        
    def upload(self, 
        bucket: str,
        endpoint_url: str,
        aws_secret_key_id: str,
        aws_secret_access_key: str,
        remote_name: str=None,
    ) -> None:

        remote_name = (self.file if not remote_name else remote_name)

        if not self.quiet: print(f'Uploading {self.outfile} transposed to {remote_name}')

        # Defines upload function and uploades combined data after all chunks are generated
        s3 = boto3.resource(
            's3',
            endpoint_url=endpoint_url,
            aws_access_key_id=aws_secret_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )

        s3.Bucket(bucket).upload_file(
            Filename=self.outfile,
            Key=remote_name,
        )