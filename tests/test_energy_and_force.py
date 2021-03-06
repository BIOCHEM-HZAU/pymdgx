import os
import mdgx
import sander
import parmed as pmd
from numpy.testing import assert_almost_equal as aa_eq

def test_eneregy_and_force():
    path = os.path.dirname(__file__) 
    
    prmtop = path + '/vAla3.prmtop'
    rst7 = path + '/vAla3.rst7'
    
    with mdgx.setup(prmtop, rst7) as context:
        mdgx_energies, mdgx_forces = context.energy_forces()
        
    pme_input = sander.pme_input()
    parm = pmd.load_file(prmtop, rst7)

    with sander.setup(prmtop, rst7, box=parm.box, mm_options=pme_input):
        
        ene, sander_forces = sander.energy_forces()
        sander_enegies = dict((att, getattr(ene, att)) for att in dir(ene) if not
            att.startswith('_'))
        
    print("")
    print("potential energy")
    print("sander_enegies")
    print(sander_enegies['tot'])
    print("mdgx_energies")
    print(mdgx_energies['eptot'])
    
    print("")
    print('forces')
    print('sander_forces, first 5 atoms')
    print(sander_forces[:15])
    print("")
    print('mdgx_forces, first 5 atoms')
    print(mdgx_forces.tolist()[:15])

    aa_eq([sander_enegies['tot'],],
          [mdgx_energies['eptot'],],
          decimal=4)

if __name__ == '__main__':
    test_eneregy_and_force()
