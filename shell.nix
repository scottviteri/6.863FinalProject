with import <nixpkgs> {};
stdenv.mkDerivation rec {
  name = "env";
  env = buildEnv { name = name; paths = buildInputs; };
  buildInputs = [
    python
    python27Packages.nltk    
    python27Packages.numpy
    python27Packages.tkinter
    python27Packages.jupyter
    python27Packages.matplotlib
    python27Packages.ipywidgets
    pandoc
    texlive.combined.scheme-full
  ];
}

