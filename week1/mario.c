#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int halght;
    do
    {
        halght = get_int("Halght: ");
    }
    while(halght < 1 || halght > 8);

    for (int i = 0; i < halght ; i++)
    {
        for (int j = 0; j < halght; j ++)
         {
              if(i + j < halght - 1)
                printf(" ");
             else
               printf("#");
         }
         printf("\n");
    }
}