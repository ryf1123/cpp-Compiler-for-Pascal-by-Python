#include <stdio.h>
int main(){
    int i=6;
    for (;i<= 8 && i>= 6 && i!= 7; i++){
        if (i>=0){
            printf("yes\n");
        }
        else 
            printf("no\n");
    }
    return 0;
}
