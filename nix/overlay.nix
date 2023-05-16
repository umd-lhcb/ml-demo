final: prev:

{
  pythonOverrides = prev.lib.composeExtensions prev.pythonOverrides (finalPy: prevPy: {
    correctionlib = finalPy.callPackage ./correctionlib { };
    dask-histogram = finalPy.callPackage ./dask-histogram { };
    cloudpickle = finalPy.callPackage ./cloudpickle { };
    coffea = finalPy.callPackage ./coffea { }; # the main thing

    # update
    dask = finalPy.callPackage ./dask { };
    dask-awkward = finalPy.callPackage ./dask-awkward { };
    llvmlite = finalPy.callPackage ./llvmlite {
      llvm = final.llvm_14;
    };
    numba = finalPy.callPackage ./numba { };

    # override
    awkward-cpp = prevPy.awkward-cpp.overridePythonAttrs (old: rec {
      version = "15";
      src = prevPy.fetchPypi {
        pname = old.pname;
        version = version;
        sha256 = "sha256-9sgl2y25gfhSkD2VdKBwFcXVPvjkYwdy8Yx/FnBFqg0=";
      };
    });
    awkward = prevPy.awkward.overridePythonAttrs (old: rec {
      version = "2.2.0";
      src = prevPy.fetchPypi {
        pname = old.pname;
        version = version;
        sha256 = "sha256-F6hTt0s5JfERbYei0EnSMPfReRd/s2+BlBMY58VFqT0=";
      };
    });
    uproot = prevPy.uproot.overridePythonAttrs (old: rec {
      version = "5.0.7";
      src = prevPy.fetchPypi {
        pname = old.pname;
        version = version;
        sha256 = "sha256-u/GY/XpyMDS7YjeIOIXzn11CwusMqG8yZmnwqsg66uI=";
      };
    });
  });

  python3 = prev.python3.override { packageOverrides = final.pythonOverrides; };
}
