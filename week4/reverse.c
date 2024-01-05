#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#include "wav.h"

int check_format(WAVHEADER header);
int get_block_size(WAVHEADER header);

int main(int argc, char *argv[])
{
   if  (argc != 3)
   {
     printf("Usage: reverse input.wav output.wav\n");
     return 1;
   }

   char *infile = argv[1];
   FILE *file = fopen(infile,"rb");
   if(file == NULL)
   {
      printf("Coud not open.%s\n",infile);
      return 1;
   }
   WAVHEADER header;

   fread(&header,sizeof(WAVHEADER),1,file);


    // Ensure proper usage
    // TODO #1
      if(check_format(header) == 0)
      {
        printf("Not a Wave file\n");
        return 1;
      }
      if (header.audioFormat != 1)
      {
        printf("Not a Wave file\n");
        return 1;
      }

    // Open input file for reading
    // TODO #2
   char *outfile = argv[2];

   FILE *outptr = fopen(outfile,"wb");
   if(outptr == NULL)
   {
      printf("Coud not open.%s\n",outfile);
      return 1;
   }
    // Read header
    // TODO #3

    // Use check_format to ensure WAV format
    // TODO #4

    // Open output file for writing
    // TODO #5

    // Write header to file
    // TODO #6
    fwrite(&header,sizeof(WAVHEADER),1,outptr);
    // Use get_block_size to calculate size of block
    // TODO #7
  int size = get_block_size(header);

    // Write reversed audio to file
    // TODO #8
    if(fseek(file,size,SEEK_END))
    {
        return 1;
    }

    BYTE buffer[size];
    while(ftell(file) - size > sizeof(header))
    {
        if(fseek(file, - 2 * size,SEEK_CUR))
        {
            return 1;
        }
        fread(buffer,size,1,file);
        fwrite(buffer,size,1,outptr);
    }

    fclose(file);
    fclose(outptr);


}

int check_format(WAVHEADER header)
{
    if (header.format[0] == 'W' && header.format[1] == 'A' && header.format[2] == 'V' && header.format[3] == 'E')
    {
        return 1;
    }
 return 0;
}

int get_block_size(WAVHEADER header)
{
    int size = header.numChannels *header.bitsPerSample / 8 ;
    return size;
}