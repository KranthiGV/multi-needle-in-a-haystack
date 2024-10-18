import csv
import os
from extractors.extractor import extract_multi_needle
from extractors.utils import read_file
from extractors.models import TechCompany

# Define the haystack and example needles
# haystack = """Ryoshi, based in Neo Tokyo, Japan, is a private quantum computing firm founded in 2031, currently valued at $8.7 billion with 1,200 employees focused on quantum cryptography.

#         ChronosTech, located in New Shanghai, Earth, was founded in 2077,
#         employs 2,800 people, and focuses on time-manipulation devices,
#         with a public status and a valuation of $6.2 billion.

#         Quantum Forge, a public company located in Orion City, Earth, was
#         founded in 2030 and currently employs 12,500 people, with a
#         valuation of $15.4 billion focused on quantum computing
#         advancements.
#         """
haystack = read_file("data/haystack.txt")
lines = haystack.splitlines()
lines = lines[47_000:48_000]
# lines = lines[47_000:51_000]
haystack = "\n".join(lines)


example_needles = [
    """Luna Dynamics, headquartered in Nova Europa, Moon, is a public
aerospace engineering firm founded in 2065, employing 9,200
workers with a valuation of $9.7 billion, focusing on lunar
habitat construction.""",
    """Stellar Innovations, located in Titan City, Saturn, has been a
public company since 2085, specializing in advanced materials
research, employing 3,300 people, and valued at $4.8 billion.""",
    """NeuroLink Systems, a private company based in Gaia, Earth, was
founded in 2045, employing 1,500 employees with a valuation of
$3.6 billion, focusing on neural interface technologies.""",
    """Zenith Robotics, a public robotics manufacturing company
headquartered in Red Sands, Mars, was founded in 2060 and employs
8,400 people with a current valuation of $11.3 billion.""",
    """Galactic BioTech, located in Celestial City, Earth, has been a
public company since 2070, specializing in genetic engineering,
employing 5,200 workers and valued at $7.5 billion.""",
    """Quantum Horizons, based in Aurora Base, Pluto, is a private
company founded in 2090, focusing on quantum encryption, with
2,200 employees and a valuation of $2.9 billion.""",
    """Solara Ventures, headquartered in Solaris, Mercury, is a public
company founded in 2082, with 6,500 employees and a valuation of
$10.5 billion, specializing in solar energy harvesting
technologies.""",
    """Orbitronix, based in Cosmo City, Earth, is a public satellite
manufacturing company founded in 2040, employing 10,300 workers
with a valuation of $14.6 billion, focusing on orbital
infrastructure development.""",
    """HyperDrive Systems, a private company located in Velocity Point,
Mars, was founded in 2078, employing 980 people with a valuation
of $1.8 billion, focusing on propulsion technologies for
interplanetary travel.""",
    """BioSphere Technologies, based in Eden Colony, Venus, is a public
company founded in 2067, employing 3,700 people with a valuation
of $6.4 billion, focusing on sustainable habitat systems for
extreme environments.""",
]

# Execute the extraction
companies = extract_multi_needle(TechCompany, haystack, example_needles)

# Define output paths
markdown_path = "output/extract.md"
csv_path = "output/extract.csv"

# Ensure the output directory exists
os.makedirs(os.path.dirname(markdown_path), exist_ok=True)

# Write to markdown file
with open(markdown_path, "w") as md_file:
    for company in companies:
        md_file.write(f"## {company.name}\n")
        md_file.write(f"- **Location**: {company.location}\n")
        md_file.write(f"- **Employee Count**: {company.employee_count}\n")
        md_file.write(f"- **Founding Year**: {company.founding_year}\n")
        md_file.write(f"- **Public**: {'Yes' if company.is_public else 'No'}\n")
        md_file.write(f"- **Valuation**: ${company.valuation} billion\n")
        md_file.write(f"- **Primary Focus**: {company.primary_focus}\n\n")

# Write to CSV file
with open(csv_path, "w", newline="") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(
        [
            "Name",
            "Location",
            "Employee Count",
            "Founding Year",
            "Public",
            "Valuation (in billion $)",
            "Primary Focus",
        ]
    )
    for company in companies:
        writer.writerow(
            [
                company.name,
                company.location,
                company.employee_count,
                company.founding_year,
                "Yes" if company.is_public else "No",
                company.valuation,
                company.primary_focus,
            ]
        )
