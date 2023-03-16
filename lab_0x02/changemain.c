#include <stdio.h>

long getfilesize(const char* fname)
{
	FILE* fp;
	fp = fopen(fname, "r");
	fseek(fp, 0, SEEK_END);
	long sz = ftell(fp);
	fclose(fp);
	return sz;
}

int main()
{
	long fsize = getfilesize("main");

	FILE* fp;
	fp = fopen("main", "r");
	char fstr[fsize];
	fread(fstr, 1, fsize, fp);
	fclose(fp);
	
	// Wrong -> 0x2009 - 0x11f2 = 0xe17
	char str1[7] = { 0x48, 0x8d, 0x3d, 0x17, 0x0e, 0x00, 0x00 };
	int j=0;
	for(int i=4587;i<4594;i++){
		fstr[i] = str1[j];
		j++;
	}
	
	// Correct -> 0x2012 - 0x11e4 = 0xe2e
	char str2[7] = { 0x48, 0x8d, 0x3d, 0x2e, 0x0e, 0x00, 0x00 };
	j=0;
	for(int i=4573;i<4580;i++){
		fstr[i] = str2[j];
		j++;
	}
	
	fp = fopen("cp_main", "w");
	fwrite(fstr, 1, fsize, fp);
	fclose(fp);

	return 0;
}

