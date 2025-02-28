import csv
import io
import click
from typing import Any, Dict
from rich.console import Console
from . import OutputFormatter

console = Console(stderr=True) # use stderr for status messages

class CsvFormatter(OutputFormatter):
    """Formats results as CSV."""

    name = "csv"
    description = "Format results as CSV"
    file_extension = "csv"

    def format(self, results: Dict[str, Any], is_unchecked: bool) -> str:
        """Format results as a CSV string.

        Args:
            results: Dictionary of results to format

        Returns:
            CSV-formatted string
        """
        col = [k for k in results.keys()]
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=col)

       
        if(is_unchecked):
           
            # Write header and rows
            writer.writeheader()
            writer.writerow(results)
            return output.getvalue()
        
        else:
            try:
                rows = [j for j in results.values() if type(j)!= int and type(j)!= int]
                print(rows)
                for row in rows:
                    if(len(row)>1):
                        print(len(row))
                        raise Exception 
                
                # Write header and rows
                writer.writeheader()
                writer.writerows(results)
                return output.getvalue()
            except Exception as e:
                console.print(f"[red]Data is nested try with -u or --unchecked flag :{e}[/red]")
                raise click.Abort() from e
            
       
        
