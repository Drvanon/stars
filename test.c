#include <math.h>
#include <stdio.h>
#include <stdlib.h>

float *createNebulaImage(int width, int height, int clouds[][2], int size) {
    float *buffer = (float *) malloc(width * height * sizeof(float));

    for (int i=0;i<width;i++) {
        for (int j=0;j<height;j++){
            float sum=0;

            for (int ci=0;ci<size;ci++) {
                int diffx = i - clouds[ci][0];
                int diffy = j - clouds[ci][1];

                sum += sqrt(pow(diffx, 2)+ pow(diffy, 2));
            }

            float strength;
            if (sum == 0) {
                strength = 1;
            } else {
                strength = 1/sum;
            }

            strength = fmin(1, fmax(0, strength));

            buffer[j*width + i] = strength;
        }
    }

    return buffer;
}

int main(int argsCount, char **args) {
    int clouds[1][2]  = {
        {25, 25}
    };

    int width, height;
    width = 500;
    height = 500;

    float *buffer = createNebulaImage(width, height, clouds, 1);
    for (int i=0;i<width;i++)  {
        for (int j=0;j<height;j++) {
            printf("%f ", buffer[j*width + i]);
        }
        printf("\n");
    }

    return 0;
}

