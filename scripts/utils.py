import base64
import os

import pandas as pd


def save_file(
    name, content, directory, subdir=None, file_type=None, model=None, state=None
):
    """
    Decode and store a file uploaded with Plotly Dash.
    Args:
        name: filename
        content: file content
        directory: session directory
        subdir: subdirectory within session directory
        file_type: type of file ('pdb', 'saxs')
        model: model type ('kds_saxs_mon_oligomer', 'kds_saxs_oligomer_fitting')
        state: state identifier ('monomer', 'oligomer', 'receptor', etc.)
    """
    if file_type == "pdb":
        if model == "kds_saxs_mon_oligomer":
            # Handle monomer/oligomer states
            state_dir = "monomer" if state == "monomer" else "oligomer"
            save_dir = os.path.join(directory, "pdbs", state_dir)
        else:
            # Handle protein binding states
            if state == "receptor":
                save_dir = os.path.join(directory, "pdbs", "receptor")
            elif state == "ligand":
                save_dir = os.path.join(directory, "pdbs", "ligand")
            else:
                save_dir = os.path.join(directory, "pdbs", "receptor_ligand")
    else:
        save_dir = os.path.join(directory, subdir) if subdir else directory

    os.makedirs(save_dir, exist_ok=True)

    data = content.encode("utf8").split(b";base64,")[1]
    file_path = os.path.join(save_dir, name)
    with open(file_path, "wb") as fp:
        fp.write(base64.decodebytes(data))
    return file_path


def get_session_path(session_dir, subdir):
    """Get full path for a subdirectory in session directory"""
    path = os.path.join(session_dir, subdir)
    os.makedirs(path, exist_ok=True)
    return path


def uploaded_files(directory):
    """List the files in the upload directory."""
    files = []
    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)
        if os.path.isfile(path):
            files.append(filename)
    return files


def truncate_filename(filename, max_length=50):
    if len(filename) <= max_length:
        return filename
    name, extension = os.path.splitext(filename)
    truncated = name[: max_length - 3 - len(extension)] + "..." + extension
    return truncated


def format_concentration(concentration, precision=6):
    """
    Format concentration value consistently throughout the application.
    Args:
        concentration (float or str): The concentration value
        precision (int): Number of decimal places to keep
    Returns:
        str: Formatted concentration string
    """
    if isinstance(concentration, pd.DataFrame):
        concentration = concentration["concentration"].iloc[0]
    return f"{float(concentration):.{precision}g}"


def get_state_from_index(selected_model, index, n_value):
    if selected_model == "kds_saxs_mon_oligomer":
        return "monomer" if index == 0 else "oligomer"
    else:
        if index == 0:
            return "receptor"
        elif index == n_value + 1:
            return "ligand"
        else:
            return f"receptor_ligand_{index}"
