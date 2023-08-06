#include <Python.h>


static PyObject *inspect(PyObject *self, PyObject *args)
{
    PyLongObject *pObj = NULL;

    /* Parse arguments */
    if (!PyArg_ParseTuple(args, "O", &pObj))
    {
        PyErr_SetString(PyExc_ValueError, "Expected function argument: pObj.");
        return NULL;
    }

    PyObject *dict = PyDict_New();
    PyObject *ob_base_dict = PyDict_New();
    PyObject *ob_base_nested_dict = PyDict_New();

    uint32_t digit_arr_size = labs(pObj->ob_base.ob_size);
    PyObject *list = PyList_New(digit_arr_size);

    PyObject *ob_base_key = PyUnicode_FromString("ob_base");
    PyObject *ob_size_key = PyUnicode_FromString("ob_size");
    PyObject *ob_refcnt_key = PyUnicode_FromString("ob_refcnt");
    PyObject *ob_type_key = PyUnicode_FromString("ob_type");
    PyObject *ob_digit_key = PyUnicode_FromString("ob_digit");

    PyDict_SetItem(dict, ob_base_key, ob_base_dict);
    PyDict_SetItem(ob_base_dict, ob_base_key, ob_base_nested_dict);
    PyDict_SetItem(ob_base_nested_dict, ob_refcnt_key, PyLong_FromLong(pObj->ob_base.ob_base.ob_refcnt));
    PyDict_SetItem(ob_base_nested_dict, ob_type_key, PyUnicode_FromString(pObj->ob_base.ob_base.ob_type->tp_name));
    PyDict_SetItem(dict, ob_size_key, PyLong_FromLong(pObj->ob_base.ob_size));
    PyDict_SetItem(dict, ob_digit_key, list);
    for (Py_ssize_t i = 0; i < digit_arr_size; i++)
    {
        PyList_SetItem(list, i, PyLong_FromLong(pObj->ob_digit[i]));
    }

    return dict;
}

static PyObject *get_parts(PyObject *self, PyObject *args)
{
    PyLongObject *pObj = NULL;

    /* Parse arguments */
    if (!PyArg_ParseTuple(args, "O", &pObj))
    {
        PyErr_SetString(PyExc_ValueError, "Expected function argument: pObj.");
        return NULL;
    }

    uint32_t digit_arr_size = labs(pObj->ob_base.ob_size);
    PyObject *list = PyList_New(digit_arr_size);

    for (Py_ssize_t i = 0; i < digit_arr_size; i++)
    {
        PyList_SetItem(list, i, PyLong_FromLong(pObj->ob_digit[i]));
    }

    return list;
}

static PyMethodDef methods[] = {
    {"inspect", inspect, METH_VARARGS, "Returns object info dict."},
    {"get_parts", get_parts, METH_VARARGS, "Returns object's ob_digit elements list."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef pyobjinfo = {
    PyModuleDef_HEAD_INIT,
    "pyobjinfo",
    "Object stats info",
    -1,
    methods};

PyMODINIT_FUNC PyInit_pyobjinfo(void)
{
    return PyModule_Create(&pyobjinfo);
}
