"""
This file is autogenerated from an ImageJ plugin generation pipeline.
"""

from bfio.bfio import BioReader, BioWriter
import argparse
import logging
import os
import numpy as np
from pathlib import Path
import ij_converter
import jpype, imagej, scyjava
import typing, os

# Import environment variables
POLUS_LOG = getattr(logging, os.environ.get("POLUS_LOG", "INFO"))
POLUS_EXT = os.environ.get("POLUS_EXT", ".ome.tif")

# Initialize the logger
logging.basicConfig(
    format="%(asctime)s - %(name)-8s - %(levelname)-8s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
)
logger = logging.getLogger("main")
logger.setLevel(POLUS_LOG)


def main(
    _opName: str,
    _in1: Path,
    _in2: str,
    _sigma: str,
    _out: Path,
) -> None:

    """Initialize ImageJ"""
    # Bioformats throws a debug message, disable the loci debugger to mute it
    def disable_loci_logs():
        DebugTools = scyjava.jimport("loci.common.DebugTools")
        DebugTools.setRootLevel("WARN")

    scyjava.when_jvm_starts(disable_loci_logs)

    # This is the version of ImageJ pre-downloaded into the docker container
    logger.info("Starting ImageJ...")
    ij = imagej.init(
        "sc.fiji:fiji:2.1.1+net.imagej:imagej-legacy:0.37.4", headless=True
    )
    # ij_converter.ij = ij
    logger.info("Loaded ImageJ version: {}".format(ij.getVersion()))

    """ Validate and organize the inputs """
    args = []
    argument_types = []
    arg_len = 0

    # Validate opName
    opName_values = [
        "DefaultDerivativeGauss",
    ]
    assert _opName in opName_values, "opName must be one of {}".format(opName_values)

    # Validate in1
    in1_types = {
        "DefaultDerivativeGauss": "RandomAccessibleInterval",
    }

    # Check that all inputs are specified
    if _in1 is None and _opName in list(in1_types.keys()):
        raise ValueError("{} must be defined to run {}.".format("in1", _opName))
    elif _in1 != None:
        in1_type = in1_types[_opName]

        # switch to images folder if present
        if _in1.joinpath("images").is_dir():
            _in1 = _in1.joinpath("images").absolute()

        args.append([f for f in _in1.iterdir() if f.is_file()])
        arg_len = len(args[-1])
    else:
        argument_types.append(None)
        args.append([None])

    # Validate in2
    in2_types = {
        "DefaultDerivativeGauss": "int[]",
    }

    # Check that all inputs are specified
    if _in2 is None and _opName in list(in2_types.keys()):
        raise ValueError("{} must be defined to run {}.".format("in2", _opName))
    else:
        in2 = None

    # Validate sigma
    sigma_types = {
        "DefaultDerivativeGauss": "double[]",
    }

    # Check that all inputs are specified
    if _sigma is None and _opName in list(sigma_types.keys()):
        raise ValueError("{} must be defined to run {}.".format("sigma", _opName))
    else:
        sigma = None

    for i in range(len(args)):
        if len(args[i]) == 1:
            args[i] = args[i] * arg_len

    """ Set up the output """
    out_types = {
        "DefaultDerivativeGauss": "RandomAccessibleInterval",
    }

    """ Run the plugin """
    try:
        for ind, (in1_path,) in enumerate(zip(*args)):
            if in1_path != None:

                # Load the first plane of image in in1 collection
                logger.info("Processing image: {}".format(in1_path))
                in1_br = BioReader(in1_path)

                # Convert to appropriate numpy array
                in1 = ij_converter.to_java(
                    ij, np.squeeze(in1_br[:, :, 0:1, 0, 0]).astype(np.float64), in1_type
                )
                metadata = in1_br.metadata
                fname = in1_path.name
                dtype = ij.py.dtype(in1)
                # Save the shape for out input
                shape = ij.py.dims(in1)
            if _in2 is not None:
                in2 = ij_converter.to_java(ij, _in2, in2_types[_opName], dtype)

            if _sigma is not None:
                sigma = ij_converter.to_java(ij, _sigma, sigma_types[_opName], dtype)

            # Generate the out input variable if required
            out_input = ij_converter.to_java(
                ij, np.zeros(shape=shape, dtype=dtype), "IterableInterval"
            )

            logger.info("Running op...")
            if _opName == "DefaultDerivativeGauss":
                out = ij.op().filter().derivativeGauss(out_input, in1, in2, sigma)

            logger.info("Completed op!")
            if in1_path != None:
                in1_br.close()

            # Saving output file to out
            logger.info("Saving...")
            out_array = ij_converter.from_java(ij, out, out_types[_opName])
            bw = BioWriter(_out.joinpath(fname), metadata=metadata)
            bw.Z = 1
            bw.dtype = out_array.dtype
            bw[:] = out_array.astype(bw.dtype)
            bw.close()

    except:
        logger.error("There was an error, shutting down jvm before raising...")
        raise

    finally:
        # Exit the program
        logger.info("Shutting down jvm...")
        del ij
        jpype.shutdownJVM()
        logger.info("Complete!")


if __name__ == "__main__":

    """Setup Command Line Arguments"""
    logger.info("Parsing arguments...")
    parser = argparse.ArgumentParser(
        prog="main",
        description="This plugin applies the nth derivative of a Gaussian to an input collection.",
    )

    # Add command-line argument for each of the input arguments
    parser.add_argument(
        "--opName",
        dest="opName",
        type=str,
        help="Op overloading method to perform",
        required=True,
    )
    parser.add_argument(
        "--inpDir",
        dest="in1",
        type=str,
        help="Collection to be processed by this plugin",
        required=False,
    )
    parser.add_argument(
        "--derivatives",
        dest="in2",
        type=str,
        help="Array of nth derivatives of the Gaussians",
        required=False,
    )
    parser.add_argument(
        "--sigma",
        dest="sigma",
        type=str,
        help="The standard deviation of the Gaussians",
        required=False,
    )

    # Add command-line argument for each of the output arguments
    parser.add_argument(
        "--outDir", dest="out", type=str, help="Output collection", required=True
    )

    """ Parse the arguments """
    args = parser.parse_args()

    # Input Args
    _opName = args.opName
    logger.info("opName = {}".format(_opName))

    _in1 = Path(args.in1)
    logger.info("inpDir = {}".format(_in1))

    _in2 = args.in2
    logger.info("derivatives = {}".format(_in2))

    _sigma = args.sigma
    logger.info("sigma = {}".format(_sigma))

    # Output Args
    _out = Path(args.out)
    logger.info("outDir = {}".format(_out))

    main(_opName=_opName, _in1=_in1, _in2=_in2, _sigma=_sigma, _out=_out)