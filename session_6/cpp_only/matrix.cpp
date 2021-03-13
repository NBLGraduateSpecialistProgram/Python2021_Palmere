// matrix.h
#include <iostream>
class Matrix{
    public:
        int size;
        int **m;
    
        Matrix(int s); // Constructor
        void display();
        void random_binary();
        
};

// matrtix.cpp
Matrix::Matrix(int s) {

    Matrix::size = s;
    Matrix::m = new int *[Matrix::size];

    for (int i = 0; i < Matrix::size; i++){
        Matrix::m[i] = new int[Matrix::size];
    }

    for (int i = 0; i < Matrix::size; i++){
        for (int j = 0; j < Matrix::size; j++){
            Matrix::m[i][j] = 0;
        }
    }
}

void Matrix::display(){
    for (int i = 0; i < Matrix::size; i++){
        for (int j = 0; j < Matrix::size; j++){
            std::cout << Matrix::m[i][j] << " ";
        }
        std::cout << std::endl;
    }
}

void Matrix::random_binary(){
    for (int i = 0; i < Matrix::size; i++){
        for (int j = 0; j < Matrix::size; j++){
            Matrix::m[i][j] = rand() % 2; // 0 or 1
        }
    }
    
}

// Where our program starts
int main(){
    
    Matrix m(25); // Generate a 10x10 sized matrix called 'm'
    do{
        m.random_binary(); // Make random ones and zeros within the matrix
        m.display(); // print this matrix object
    } while (true); // Do it forever
    
}
