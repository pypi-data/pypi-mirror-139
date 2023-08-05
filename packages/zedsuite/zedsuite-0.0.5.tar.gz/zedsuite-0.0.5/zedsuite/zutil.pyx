import os
import ctypes
import pandas as pd
from zedsuite.utils import RANDOM_NAME, CythonWrapper
from cython import boundscheck, nonecheck, wraparound, cdivision
from cython cimport sizeof
from zedsuite.zutil cimport _llk, _lsmash, _prun, _drawPFSA
from libc.stdlib cimport malloc, free
from libc.string cimport strcpy


class Llk(CythonWrapper):
    def __init__(
        self,
        helpmsg: bool = False,
        version: bool = False,
        data: [[]] = None,
        seqfile: str = None,
        data_dir: str = None,
        data_len: ctypes.c_uint = None,
        pfsafile: str = None
    ) -> None:

        super().__init__()

        self.argc = 1
        self.argv = ['llk']

        # Program information:
        if helpmsg:
            self._add_flag("-h")
        if version:
            self._add_flag("-V")

        # Usage:
        self.data = None
        if data is not None:
            if type(data) is pd.DataFrame or type(data) is pd.Series:
                self.data = data.values.tolist()
            else:
                self.data = data
        if seqfile is not None:
            self._add_param("-s", seqfile)
        if data_dir is not None:
            self._add_param("-D", data_dir)
        if data_len is not None:
            self._add_param("-x", str(data_len))
        if pfsafile is not None:
            self._add_param("-f", pfsafile)

        # Results
        self.llk_vec = None

    @boundscheck(False)
    @nonecheck(False)
    @wraparound(False)
    @cdivision(True)
    def run(self):
        # convert self.argv to a char** to be passed to wrapped c++ function
        argv = <char **> malloc(self.argc * sizeof(ctypes.c_char_p))
        for i, arg in enumerate(self.argv):
            argv[i] = <char *> malloc(len(arg) * sizeof(char))
            strcpy(argv[i], bytes(arg, 'utf-8'))

        # _llk() defined in _llk.cc
        self.llk_vec = _llk(self.argc, argv, self.data)

        for i in range(self.argc):
            free(argv[i])
        free(argv)

        return self.llk_vec


class Lsmash(CythonWrapper):
    def __init__(
        self,
        helpmsg: bool = False,
        version: bool = False,
        data: [[]] = None,
        seqfile: str = None,
        data_dir: str = None,
        data_type: str = None,
        data_len: ctypes.c_uint = None,
        partition: list = None,
        derivative: bool = None,
        pfsafiles: list = None,
        timer: bool = None,
        sae: bool = None,
        repeat: ctypes.c_uint = None,
        outfile: str = None,
        random_mc: ctypes.c_uint = None,
        print_mc: bool = None,
    ) -> None:

        super().__init__()

        self.argc = 1
        self.argv = ['lsmash']

        # Program information:
        if helpmsg:
            self._add_flag("-h")
        if version:
            self._add_flag("-V")

        # Usage:
        self.data = None
        if data is not None:
            if type(data) is pd.DataFrame or type(data) is pd.Series:
                self.data = data.values.tolist()
            else:
                self.data = data
        if seqfile is not None:
            self._add_param("-f", seqfile)
        if data_dir is not None:
            self._add_param("-D", data_dir)
        if data_type is not None:
            self._add_param("-T", data_type)
        if data_len is not None:
            self._add_param("-x", str(data_len))
        if partition is not None:
            self._add_param("-P", " ".join([str(n) for n in partition]))
        if derivative is not None:
            self._add_param("-u", str(derivative))
        if pfsafiles is not None:
            self._add_param("-F", " ".join([str(n) for n in pfsafiles]))
        if timer is not None:
            self._add_param("-t", str(timer))
        if sae is not None:
            self._add_param("-S", str(sae))
        if repeat is not None:
            self._add_param("-n", str(repeat))
        if outfile is not None:
            self._add_param("-o", outfile)
        if random_mc is not None:
            self._add_param("-R", str(random_mc))
        if print_mc is not None:
            self._add_param("-m", str(print_mc))

        # Results
        self.dist_matrix = None

    @boundscheck(False)
    @nonecheck(False)
    @wraparound(False)
    @cdivision(True)
    def run(self):
        # convert self.argv to a char** to be passed to wrapped c++ function
        cdef char** argv = <char **> malloc(self.argc * sizeof(ctypes.c_char_p))
        for i, arg in enumerate(self.argv):
            argv[i] = <char *> malloc(len(arg) * sizeof(char))
            strcpy(argv[i], bytes(arg, 'utf-8'))

        # _lsmash() defined in _lsmash.cc
        self.dist_matrix = _lsmash(self.argc, argv, self.data)

        # testing parallelization without GIL
        # cdef unsigned int argc = self.argc
        # cdef matrix_dbl dist_matrix
        # openmp.omp_set_dynamic(1)
        # with nogil, parallel():
        #     dist_matrix = _lsmash(argc, argv)
        # self.dist_matrix = dist_matrix

        for i in range(self.argc):
            free(argv[i])
        free(argv)

        return self.dist_matrix


class Prun(CythonWrapper):
    def __init__(
        self,
        helpmsg: bool = False,
        version: bool = False,
        pfsafile: str = None,
        data_len: ctypes.c_uint = None,
        num_repeats: ctypes.c_uint = None,
        outfile: str = None,
        show_gamma: bool = None,
        show_pi: bool = None,
        show_stationary: bool = None,
        show_machine: bool = None,
        graph_name: str = None,
        graph_type: str = None,
        draw_graph: bool = None,
    ) -> None:

        super().__init__()

        self.argc = 1
        self.argv = ['prun']

        # Program information:
        if helpmsg:
            self._add_flag("-h")
        if version:
            self._add_flag("-V")

        # Usage:
        if pfsafile is not None:
            self._add_param("-f", pfsafile)
        if data_len is not None:
            self._add_param("-l", str(data_len))
        if num_repeats is not None:
            self._add_param("-n", str(num_repeats))
        if outfile is not None:
            self._add_param("-o", outfile)
        if show_gamma is not None:
            self._add_param("-G", str(show_gamma))
        if show_pi is not None:
            self._add_param("-P", str(show_pi))
        if show_stationary is not None:
            self._add_param("-S", str(show_stationary))
        if show_machine is not None:
            self._add_param("-M", str(show_machine))
        if graph_name is not None:
            self._add_param("-R", graph_name)
        if graph_type is not None:
            self._add_param("-T", graph_type)
        if draw_graph is not None:
            self._add_param("-g", str(draw_graph))


    def run(self):
        # convert self.argv to a char** to be passed to wrapped c++ function
        argv = <char **> malloc(self.argc * sizeof(ctypes.c_char_p))
        for i, arg in enumerate(self.argv):
            argv[i] = <char *> malloc(len(arg) * sizeof(char))
            strcpy(argv[i], bytes(arg, 'utf-8'))

        # _prun() defined in _prun.cc
        self.seq = _prun(self.argc, argv)

        for i in range(self.argc):
            free(argv[i])
        free(argv)

        return self.seq


class DrawPFSA(CythonWrapper):
    def __init__(
        self,
        helpmsg: bool = False,
        version: bool = False,
        pfsafile: str = None,
        data_len: ctypes.c_uint = None,
        graphpref: str = None,
        dotname: str = None,
        graph_type: int = None,
        show_machine: bool = None,
        show_inverse_machine: bool = None,
        show_stationary: bool = None,
        show_pi: bool = None,
        show_gamma: bool = None,

    ) -> None:

        super().__init__()
        self.argc = 1
        self.argv = ['drawpfsa']

        # Program information:
        if helpmsg:
            self._add_flag("-h")
        if version:
            self._add_flag("-V")

        # Usage:
        if pfsafile is not None:
            self._add_param("-c", pfsafile)
        if data_len is not None:
            self._add_param("-x", str(data_len))
        self.graphpref = None
        if graphpref is not None:
            self.graphpref = graphpref
            self._add_param("-N", graphpref)
        if dotname is not None:
            self._add_param("-d", dotname)
        if graph_type is not None:
            self._add_param("-D", str(graph_type))
        if show_machine is not None:
            self._add_param("-P", str(show_machine))
        if show_inverse_machine is not None:
            self._add_param("-I", str(show_inverse_machine))
        if show_stationary is not None:
            self._add_param("-S", str(show_stationary))
        if show_pi is not None:
            self._add_param("-p", str(show_pi))
        if show_gamma is not None:
            self._add_param("-G", str(show_gamma))


    def run(self):
        # convert self.argv to a char** to be passed to wrapped c++ function
        argv = <char **> malloc(self.argc * sizeof(ctypes.c_char_p))
        for i, arg in enumerate(self.argv):
            argv[i] = <char *> malloc(len(arg) * sizeof(char))
            strcpy(argv[i], bytes(arg, 'utf-8'))

        # _drawPFSA() defined in _drawPFSA.cc
        _drawPFSA(self.argc, argv)

        for i in range(self.argc):
            free(argv[i])
        free(argv)

        pref = self.graphpref if self.graphpref is not None else "pfsa"
        return f"{pref}.png"
