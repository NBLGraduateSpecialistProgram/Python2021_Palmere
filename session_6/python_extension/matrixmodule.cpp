/*
 * Introduction to C++ in Python
 * Robert Palmere, 2021
 * Python C API functions can be found here: https://docs.python.org/3/c-api/intro.html
 *
 */

#define PY_SSIZE_T_CLEAN

#include <iostream> // Input / output stream for printing
#include <Python.h> // Python API (contains all the declarations for goodies to create our Python module)
#include <structmember.h> // include declarations to handle attributes

typedef struct {
    PyObject_HEAD // Macro required to define the "ob_base" field of the PyObject (contains pointer to PyObject and a reference count)

    /* Type-specific fields go here. */

	int size;
	int **mat;
	PyObject *display;
	PyObject *random_binary;

} MatrixObject; // Initialize the struct after defining

static void Matrix_dealloc(MatrixObject *self){ // Method for memory deallocation
	Py_XDECREF(self->display);
	Py_XDECREF(self->random_binary);
	Py_TYPE(self)->tp_free((PyObject *) self);
}

static PyObject *Matrix_new(PyTypeObject *type, PyObject *args, PyObject *kwds){
	MatrixObject *self;
	self = (MatrixObject *) type->tp_alloc(type, 0);

	if (self != NULL){
		self->size = 0;
	}

	return (PyObject *) self; // __new__() returns self to the __init__()	
}

static int Matrix_init(MatrixObject *self){ // __init__(self)
	
	self->size = 5;
    self->mat = new int *[self->size];
    for (int i = 0; i < self->size; i++){
        self->mat[i] = new int[self->size];
    }

    for (int i = 0; i < self->size; i++){
        for (int j = 0; j < self->size; j++){
            self->mat[i][j] = 0;
        }
    }
    return 0;
}

static PyMemberDef Matrix_members[] = { // Define array member definitions for Matrix type

	{"size", T_INT, offsetof(MatrixObject, size), 0, "size of square matrix"},
	{"mat", T_INT, offsetof(MatrixObject, mat), 0, "2d array"},
	{NULL} // Sentinel (signaling the end of the array)

};

/* Note all functions for a C extension in Python need to return a PyObject (e.g. Py_RETURN_NONE if function returns void in C ) ! */
static PyObject *Matrix_display(MatrixObject *self, PyObject *Py_UNUSED(ignored)){ // Define the display() method

	for (int i = 0; i < self->size; i++){
        for (int j = 0; j < self->size; j++){
			std::cout << self->mat[i][j] << " ";
        }
		std::cout << std::endl;
    }

	Py_RETURN_NONE;
}

static PyObject *Matrix_random_binary(MatrixObject *self, PyObject *Py_UNUSED(ignored)){ // Define the random_binary() method

	for (int i = 0; i < self->size; i++){
        for (int j = 0; j < self->size; j++){
            self->mat[i][j] = rand() % 2;
        }
    }
	Py_RETURN_NONE;
}

static PyMethodDef Matrix_methods[] = { // Define array of member methods for Matrix type

	{"display", (PyCFunction) Matrix_display, METH_NOARGS, "Display the square matrix."},
	{"random_binary", (PyCFunction) Matrix_random_binary, METH_NOARGS, "Matrix filled randomly with 0 or 1."},
	{NULL} // Sentinel (signaling the end of the array)

};

static PyTypeObject MatrixType = {
    PyVarObject_HEAD_INIT(NULL, 0) // Intialize the "ob_base" field values (standard)
    .tp_name = "matrix.Matrix", // The name of the type. May appear as matrix.matrix() in error messages
    .tp_doc = "Matrix object", // the __doc__ string for the type
    .tp_basicsize = sizeof(MatrixObject), // tells Python how much memory to allocate for the type 
    .tp_itemsize = 0, // Should be zero as we are defining a type and this is to be defined otherwise for variable-sized objects
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE, // Constant (defines members up to Python3.3)
	.tp_new = Matrix_new, // tp_new calls tp_alloc slot to allocate memory for __new__() in Python
	.tp_init = (initproc) Matrix_init, // __init__()
	.tp_dealloc = (destructor) Matrix_dealloc,
	.tp_members = Matrix_members, // add members
	.tp_methods = Matrix_methods, // add methods
};

static PyModuleDef matrixmodule = {
    PyModuleDef_HEAD_INIT,
    .m_name = "matrix",
    .m_doc = "Create a matrix object for binary",
    .m_size = -1,
};

PyMODINIT_FUNC
PyInit_matrix(void)
{
    PyObject *m; // Delcare "m" as PyObject struct pointer
    if (PyType_Ready(&MatrixType) < 0){
		std::cout << "PyType not ready." << std::endl;
        return NULL;
	}
    m = PyModule_Create(&matrixmodule); // "m" now points to the created matrix module
    if (m == NULL){
		std::cout << "Could not create matrixmodule as a PyModule." << std::endl;
        return NULL;
	}
    Py_INCREF(&MatrixType); // Adds the "matrix" type to the module dictionary -- i.e. we can now "import matrix ; matrix.matrix()" 
    if (PyModule_AddObject(m, "Matrix", (PyObject *) &MatrixType) < 0) { // If we can't add the the object we will remove the reference and object and return NULL
        Py_DECREF(&MatrixType);
        Py_DECREF(m);
		std::cout << "Could not add object as a PyModule." << std::endl;
        return NULL;
    }

    return m; // Return instance "m" of PyObject* 
}
