def remove_barostat(system):
    """Remove MonteCarloBarostat if present"""
    fs = system.getForces()
    for i, f in enumerate(fs):
        if (
            type(f) == openmm.openmm.openmm.MonteCarloBarostat
            or type(f) == openmm.openmm.openmm.MonteCarloAnisotropicBarostat
        ):
            system.removeForce(i)
            return
