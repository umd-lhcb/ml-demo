final: prev:

{
  pythonOverrides = prev.lib.composeExtensions prev.pythonOverrides (finalPy: prevPy: {
    coffea = finalPy.callPackage ./coffea/default.nix { };
  });
  python3 = prev.python3.override { packageOverrides = final.pythonOverrides; };
}
