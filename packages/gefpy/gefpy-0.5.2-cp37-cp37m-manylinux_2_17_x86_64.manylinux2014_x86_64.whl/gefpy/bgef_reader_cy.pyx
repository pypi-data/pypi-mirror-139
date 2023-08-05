# -*- coding: utf-8 -*-
# distutils: language=c++
# cython: language_level=3, boundscheck=False
# cython: c_string_type=unicode, c_string_encoding=utf8
# Created by huangzhibo on 2022/01/01
"""
    Provides access to the bgef_reader interface.
    For reading common bin GEF.
"""

from .bgef_reader cimport *
import numpy as np
cimport numpy as np
import array

from cython cimport view

# EXP_DTYPE = np.dtype([
#     ('x', np.uint32),
#     ('y', np.uint32),
#     ('count', np.uint32),
# ])

cdef class BgefR:
    cdef BgefReader* bgef_instance # Hold a C++ instance which we're wrapping
    cdef unsigned int exp_len
    cdef unsigned int gene_num

    def __cinit__(self, filepath, bin_size, n_thread):
        self.bgef_instance = new BgefReader(filepath, bin_size, n_thread, True)
        self.exp_len = self.bgef_instance.getExpressionNum()
        self.gene_num = self.bgef_instance.getGeneNum()

    def __init__(self, filepath, bin_size, n_thread):
        """
        A class for reading common bin GEF.

        :param filepath: Input bin GEF filepath.
        :param bin_size: Bin size.
        """
        pass

    def __dealloc__(self):
        del self.bgef_instance

    def get_expression_num(self):
        """
        Get the number of expression.
        """
        return self.bgef_instance.getExpressionNum()

    def get_cell_num(self):
        """
        Get the number of cell.
        """
        return self.bgef_instance.getCellNum()

    def get_gene_num(self):
        """
        Get the number of gene.
        """
        return self.bgef_instance.getGeneNum()

    def get_gene_names(self):
        """
        Get an array of gene names.
        """
        # cdef view.array gene_names = view.array((self.bgef_instance.getGeneNum(),),
        #                                         itemsize=32 * sizeof(char), format='32s', allocate_buffer=True)
        cdef vector[string] gene_names
        gene_names.reserve(self.gene_num)
        self.bgef_instance.getGeneNameList(gene_names)
        return np.asarray(gene_names)

    def get_cell_names(self):
        """
        Get an array of cell ids.
        """
        cdef unsigned long long int[::1] cell_names = np.empty(self.get_cell_num(), dtype=np.uint64)
        # cdef view.array gene_names = view.array((self.bgef_instance.getGeneNum(),),
        #                                    itemsize=32*sizeof(char), format='32s', allocate_buffer=True)
        self.bgef_instance.getCellNameList(&cell_names[0])
        return np.asarray(cell_names)

    def get_cell_names2(self, np.ndarray[np.ulonglong_t, ndim=1] cell_names):
        """
        Get an array of cell ids.
        """
        # cdef unsigned long long int[::1] cell_names = np.empty(self.get_cell_num(), dtype=np.uint64)
        # cdef view.array gene_names = view.array((self.bgef_instance.getGeneNum(),),
        #                                    itemsize=32*sizeof(char), format='32s', allocate_buffer=True)
        self.bgef_instance.getCellNameList(<unsigned long long int *>cell_names.data)
        # return np.asarray(cell_names)

    # def get_gene_data(self):
    #     cdef unsigned int[::1] gene_index = np.empty(self.exp_len, dtype=np.uint32)
    #     cdef vector[string] uniq_genes = self.bgef_instance.getSparseMatrixIndexesOfGene(&gene_index[0])
    #     return np.asarray(gene_index), np.asarray(uniq_genes)

    # def get_expression(self, np.ndarray[np.uint32_t, ndim = 1] expression):
    #     cdef Expression * exp = self.bgef_instance.getExpression()
    #     for i in range(self.exp_len):
    #         expression[3*i] = exp[i].x
    #         expression[3*i+1] = exp[i].y
    #         expression[3*i+2] = exp[i].count

    def get_expression(self):
        cdef view.array exp = view.array((self.exp_len,3),
                                         itemsize=4*sizeof(char), format='I', allocate_buffer=False)
        exp.data = <char*>self.bgef_instance.getExpression()
        # arr = np.asarray(exp, dtype=EXP_DTYPE)
        # arr.astype(EXP_DTYPE)
        return np.asarray(exp)

    def get_reduce_expression(self):
        cdef view.array exp = view.array((self.get_cell_num(),3),
                                         itemsize=4*sizeof(char), format='I', allocate_buffer=False)
        exp.data = <char*>self.bgef_instance.getReduceExpression()
        # arr = np.asarray(exp, dtype=EXP_DTYPE)
        # arr.astype(EXP_DTYPE)
        return np.asarray(exp)

    def get_sparse_matrix_indices(self):
        """
        Gets indices for building csr_matrix.

        Examples:
        from scipy import sparse
        sparse.csr_matrix((count, indices, indptr), shape=(cell_num, gene_num))

        :param indices:  CSR format index array of the matrix. Cell id array, the column indices, is the same size as count.
        :param indptr:   CSR format index pointer array of the matrix. indptr length = gene_num_ + 1 .
        :param count:    CSR format data array of the matrix. Expression count.
        :return: (indices, indptr, count)
        """
        cdef unsigned int[::1] indices = np.empty(self.exp_len, dtype=np.uint32)
        cdef unsigned int[::1] indptr = np.empty(self.gene_num + 1, dtype=np.uint32)
        cdef unsigned int[::1] count = np.empty(self.exp_len, dtype=np.uint32)
        self.bgef_instance.getSparseMatrixIndices(&indices[0], &indptr[0], &count[0])
        return np.asarray(indices), np.asarray(indptr), np.asarray(count)

    def get_sparse_matrix_indices2(self):
        """
        Gets indices for building csr_matrix.

        Examples:
        from scipy import sparse
        sparse.csr_matrix((count, cell_ind, gene_ind), shape=(cell_num, gene_num))

        :param cell_ind:  CSR format index array of the matrix. same size as count.
        :param gene_ind:  CSR format index array of the matrix. same size as count.
        :param count:     CSR format data array of the matrix. Expression count.
        :return: (cell_ind, gene_ind, count)
        """
        cdef unsigned int[::1] cell_ind = np.empty(self.exp_len, dtype=np.uint32)
        cdef unsigned int[::1] gene_ind = np.empty(self.exp_len, dtype=np.uint32)
        cdef unsigned int[::1] count = np.empty(self.exp_len, dtype=np.uint32)
        self.bgef_instance.getSparseMatrixIndices2(&cell_ind[0], &gene_ind[0], &count[0])
        return np.asarray(cell_ind), np.asarray(gene_ind), np.asarray(count)


    # def get_sparse_matrix_indices_of_exp(self):
    #     """
    #     Get sparse matrix indexes of expression data.
    #
    #     :return: (uniq_cell, cell_index, count)
    #     """
    #     cdef unsigned int[::1] cell_index = np.empty(self.exp_len, dtype=np.uint32)
    #     cdef unsigned int[::1] count = np.empty(self.exp_len, dtype=np.uint32)
    #     cdef vector[unsigned long long] uniq_cell = self.bgef_instance.getSparseMatrixIndicesOfExp(&cell_index[0], &count[0])
    #     return np.asarray(uniq_cell), np.asarray(cell_index), np.asarray(count)

    # def get_sparse_matrix_indices_of_gene(self):
    #     """
    #     Get gene data.
    #     :return: (gene_index, gene_names)
    #     """
    #     cdef unsigned int[::1] gene_index = np.empty(self.bgef_instance.getExpressionNum(), dtype=np.uint32)
    #     cdef view.array gene_names = view.array((self.bgef_instance.getGeneNum(),),
    #                                        itemsize=32*sizeof(char), format='32s', allocate_buffer=True)
    #
    #     self.bgef_instance.getSparseMatrixIndicesOfGene(&gene_index[0], <char*>gene_names.data)
    #     return np.asarray(gene_index), np.asarray(gene_names)


    def read_whole_exp_matrix(self,
                              unsigned int offset_x,
                              unsigned int offset_y,
                              unsigned int rows,
                              unsigned int cols,
                              string & key,
                              np.ndarray[np.uint8_t, ndim=1] matrix):
        """
        Get wholeExp matrix.

        :param offset_x: The starting position on the x-axis to be read.
        :param offset_y: The starting position on the y-axis to be read.
        :param rows:     Number of rows to read.
        :param cols:     Number of cols to read.
        :param key: MIDcount or genecount.
        :param matrix: When the value is greater than 255, it will be set to 255.
        :return:
        """
        self.bgef_instance.readWholeExpMatrix(offset_x, offset_y, rows, cols, key, <unsigned char*>matrix.data)


    def read_whole_exp_matrix_all(self, str key):
        """
        Get wholeExp matrix.

        :param key: MIDcount or genecount.
        :return: 2D Matrix: When the value is greater than 255, it will be set to 255.
        """
        cdef np.ndarray[np.uint8_t, ndim = 2] matrix = np.empty(self.get_whole_exp_matrix_shape(), dtype=np.uint8)
        self.bgef_instance.readWholeExpMatrix(key, <unsigned char*>matrix.data)
        return matrix

    def get_whole_exp_matrix_shape(self) -> np.ndarray:
        """
        Get the shape of wholeExp matrix.
        :return: [rows, cols]
        """
        cdef view.array shape = view.array((2,), itemsize=sizeof(unsigned int), format="I", allocate_buffer=False)
        shape.data = <char *>self.bgef_instance.getWholeExpMatrixShape()
        return np.asarray(shape)

    def to_gem(self, filename):
        self.bgef_instance.toGem(filename)
