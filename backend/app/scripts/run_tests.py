import typer
import pytest
import os
import coverage

def main(
    coverage_report: bool = typer.Option(False, "--coverage", "-c", help="Generate coverage report"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
    failfast: bool = typer.Option(False, "--failfast", "-f", help="Stop on first failure"),
    test_path: str = typer.Option("tests", "--path", "-p", help="Path to test files")
):
    """Run the test suite"""
    args = [test_path]
    
    if verbose:
        args.append("-v")
    if failfast:
        args.append("-x")
    
    if coverage_report:
        # Start coverage
        cov = coverage.Coverage()
        cov.start()
    
    # Run tests
    result = pytest.main(args)
    
    if coverage_report:
        # Stop coverage and generate report
        cov.stop()
        cov.save()
        
        # Generate reports
        typer.echo("\nCoverage Report:")
        cov.report()
        
        # Generate HTML report
        html_report_dir = "htmlcov"
        cov.html_report(directory=html_report_dir)
        typer.echo(f"\nHTML coverage report generated in {html_report_dir}/")
    
    raise typer.Exit(result)

if __name__ == "__main__":
    typer.run(main)