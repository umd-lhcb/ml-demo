final: prev:

{
  pythonOverrides = prev.lib.composeExtensions prev.pythonOverrides (finalPy: prevPy: {
    # add dependencies for coffea
    correctionlib = finalPy.callPackage ./correctionlib { };
    dask-histogram = finalPy.callPackage ./dask-histogram { };
    cloudpickle = finalPy.callPackage ./cloudpickle { };
    coffea = finalPy.callPackage ./coffea { }; # the main thing
  });

  python3 = prev.python3.override { packageOverrides = final.pythonOverrides; };
}
