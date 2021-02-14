

#include "stdafx.h"
#include <iostream>


char string[] = "Donde se ubicara?";
char string2[20];


void ejemplos_ubicacion()
{

	char mensaje_en_stack[]="hola reverser en stack";
	char mensaje_en_stack_sin_inicializar[100];
	char *mensaje_en_data="hola reverser en data";
	char *mensaje_en_heap;
	


	mensaje_en_heap = (char *)malloc(strlen(mensaje_en_data)+1);

	strcpy(mensaje_en_stack_sin_inicializar, "hola reverser en stack sin inicializar");
	
	strcpy(mensaje_en_heap,mensaje_en_data);

	memcpy(mensaje_en_heap+strlen("hola reverser en "),"heap",4);

	strcpy(string2,"Donde se ubicara?");

	printf("direccion mensaje_en_stack = 0x%x\n", mensaje_en_stack);
	printf("direccion mensaje_en_stack_sin_inicializar = 0x%x\n", mensaje_en_stack_sin_inicializar);
	printf("direccion mensaje_en_data = 0x%x\n", mensaje_en_data);
	printf("direccion mensaje_en_heap = 0x%x\n", mensaje_en_heap);
	printf("direccion string = 0x%x\n", string);
	printf("direccion string2 = 0x%x\n", string2);

	getchar();


}

int _tmain(int argc, _TCHAR* argv[])
{

	ejemplos_ubicacion();

	return 0;
}

