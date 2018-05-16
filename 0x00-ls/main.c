#include "hls.h"

/**
 * main - main function
 *
 * Return: success
 */
int main(void)
{
	DIR *dir;
	char *currentdir;
	struct dirent *read;

	currentdir = getenv("PWD");
	dir = opendir(currentdir);
	while ((read = readdir(dir)) != NULL)
		printf("%s ", read->d_name);
	printf("\n");
	closedir(dir);

	return (0);
}
