#include <stdio.h>

int main(int argc, char *argv[]) 
{
	int x = 0;
	if (argc > 1)
	{
		for (x=1;x<argc;x++) printf("%s \n", argv[x]);
	}
	else printf("Hello \n");
	return 0;
}
