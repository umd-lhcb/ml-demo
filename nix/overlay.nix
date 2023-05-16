final: prev:

{
  pythonOverrides = prev.lib.composeExtensions prev.pythonOverrides (finalPy: prevPy: {
    correctionlib = finalPy.callPackage ./correctionlib { };
    coffea = finalPy.callPackage ./coffea { };
  });
  python3 = prev.python3.override { packageOverrides = final.pythonOverrides; };
}
