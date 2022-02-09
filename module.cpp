#include <Python.h>

static PyObject* getPower(PyObject* self, PyObject* args)
{
    unsigned long long number;
    if (!PyArg_ParseTuple(args, "K", &number))
        return NULL;
    unsigned long counter = 0;
    while (number)
    {
        number >>= 1;
        counter++;
    }
    return PyLong_FromUnsignedLong((unsigned long)(64 - counter));
}

static PyObject* getBitsCount(PyObject* self, PyObject* args)
{
    unsigned long long number;
    if (!PyArg_ParseTuple(args, "K", &number))
        return NULL;
    unsigned long counter = 0;
    while (number)
    {
        if (number & 1)
        {
            counter++;
        }
        number >>= 1;
    }
    return PyLong_FromUnsignedLong(counter);
}

static PyMethodDef TestDLL_methods[] = {
    { "getPower", (PyCFunction)getPower, METH_VARARGS, ""},
    { "getBitsCount", (PyCFunction)getBitsCount, METH_VARARGS, ""},
    { NULL, NULL, 0, NULL }
};

static PyModuleDef TestDLL_module = {
    PyModuleDef_HEAD_INIT,
    "TestDLL",
    "C++ extension",
    -1,
    TestDLL_methods
};

PyMODINIT_FUNC PyInit_TestDLL() {
    return PyModule_Create(&TestDLL_module);
}
