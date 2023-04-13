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
	long fsize = getfilesize("task2");

	FILE* fp;
	fp = fopen("task2", "r");
	char fstr[fsize];
	fread(fstr, 1, fsize, fp);
	fclose(fp);
	
	int start = 0x11C7;
	int end = 0x12CB;
	for(int i=start; i<end; i++){
		fstr[i] = ~(fstr[i]);
	}
	
	fp = fopen("patched_task2", "w");
	fwrite(fstr, 1, fsize, fp);
	fclose(fp);

	return 0;
}

