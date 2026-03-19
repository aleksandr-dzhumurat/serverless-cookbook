import os
from pathlib import Path
from datetime import datetime

from openmm import unit


def save_simulation_metadata(protein_id: str, steps: int, sim_dir: Path, 
                           system, integrator, simulation, output_filename: str):
    """Save simulation metadata to a text file."""
    
    metadata_file = sim_dir / f"{protein_id}_metadata.txt"
    
    with open(metadata_file, 'w') as f:
        f.write("OpenMM Molecular Dynamics Simulation Metadata\n")
        f.write("=" * 50 + "\n")
        f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Protein ID: {protein_id}\n")
        f.write(f"Simulation steps: {steps}\n")
        f.write("\n")
        
        try:
            # Get final energy and other simulation properties
            state = simulation.context.getState(getEnergy=True, getPositions=True)
            potential_energy = state.getPotentialEnergy().value_in_unit(unit.kilojoules_per_mole)
            f.write(f"Final potential energy: {potential_energy:.2f} kJ/mol\n")
            
            # Get system information
            num_particles = system.getNumParticles()
            num_forces = system.getNumForces()
            f.write(f"Number of particles: {num_particles}\n")
            f.write(f"Number of force terms: {num_forces}\n")
            
            # Get integrator information
            temperature = integrator.getTemperature().value_in_unit(unit.kelvin)
            friction = integrator.getFriction().value_in_unit(1/unit.picosecond)
            step_size = integrator.getStepSize().value_in_unit(unit.picoseconds)
            f.write(f"Temperature: {temperature:.1f} K\n")
            f.write(f"Friction coefficient: {friction:.1f} ps⁻¹\n")
            f.write(f"Time step: {step_size:.3f} ps\n")
            
            # Calculate total simulation time
            total_time = steps * step_size
            f.write(f"Total simulation time: {total_time:.2f} ps\n")
            f.write("\n")
            
            # File information
            f.write("Generated Files:\n")
            f.write(f"- Trajectory: {output_filename}\n")
            f.write(f"- Processed structure: {protein_id}_processed.pdb\n")
            f.write(f"- Metadata: {protein_id}_metadata.txt\n")
            
            if os.path.exists(output_filename):
                file_size = os.path.getsize(output_filename) / 1024  # KB
                f.write(f"- Trajectory file size: {file_size:.1f} KB\n")
                
        except Exception as e:
            f.write(f"Warning: Could not retrieve simulation metadata: {e}\n")
    
    print(f"Metadata saved to {metadata_file}")
    return str(metadata_file)
