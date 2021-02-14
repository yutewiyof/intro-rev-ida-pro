// ConsoleApplication11.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <stdlib.h>
#include <Windows.h>
#include <stdio.h>

	

typedef int(*system_t)(char *);

int main()
{

	    int *Dst;
		int temp;
		system_t Dst3;
		unsigned int numero;
		LoadLibraryA("Mypepe.dll")
;

		printf("Ingrese una cantidad de numeros enteros a ingresar: \n"); 
		scanf_s("%d",&numero); 
		printf("La cantidad de enteros que va a ingresar es %d\n", numero); 


		Dst = (int *) malloc(numero*4);

		Dst3 = (system_t)&system;

		system_t *array = new system_t[4];


		array[0] = (system_t)&printf;


		printf("La direccion donde va a escribir sus enteros es 0x%x\n", Dst);
		printf("La direccion a pisar es 0x%x\n", array);

		printf("Ingrese entero\n");

		for (int i = 0; i < numero; i++) {


			scanf_s("%d", &temp);
			if (temp > 0x20) {
				memcpy(Dst, &temp, 4);
			}

			array[0]("correcto\n");
			Dst++;
		}


		getchar();

    return 0;
}

