# Copyright (C) 2022 Chi-kwan Chan
# Copyright (C) 2022 Steward Observatory
#
# This file is part of jaction.
#
# Jaction is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Jaction is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with jaction.  If not, see <http://www.gnu.org/licenses/>.


from jax import numpy as np
from jax import grad, jacfwd, jit
from jax.numpy.linalg import inv

from xaj import odeint


def ELrhs(L):

    Lx = grad(L, argnums=1)
    Lv = grad(L, argnums=2)

    Lvt = jacfwd(Lv, argnums=(0,1,2))

    @jit
    def rhs(t, xv):
        x = xv[0,:]
        v = xv[1,:]
        d = Lvt(t, x, v)
        a = inv(d[2]) @ (Lx(t, x, v) - d[0] - v @ d[1])
        return np.array([v, a])

    return rhs


def Path(L, x0, v0, h, **kwargs):
    return odeint(ELrhs(L), x0, v0, h, **kwargs)
