# Set the directory for output files
$out_dir = 'build';

# Use pdflatex as the default compiler
$pdflatex = 'pdflatex -interaction=nonstopmode -file-line-error';

# Specify the output directory for PDF files
$pdf_mode = 1; # Use PDF mode

# Set the output directory for auxiliary files
$aux_dir = "$out_dir";

# Set the output directory for log files
$log_file = "$out_dir/latexmk.log";

# Enable the use of bibtex for bibliography
$bibtex = 'bibtex';

# Clean up auxiliary files after a successful build
$clean_ext = 'aux bbl blg fdb_latexmk log out toc fls synctex.gz';

# Custom commands to run after a successful build
$clean_full_ext = 'pdf';

# Automatically clean up files in the output directory
$clean_full_ext = "aux bbl blg fdb_latexmk log out toc fls synctex.gz";

# Add build directory to the list of paths
push(@generated_exts, 'pdf');
