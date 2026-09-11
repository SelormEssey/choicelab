from __future__ import annotations

import hashlib
import json

from .models import OptionDefinition, TrialDefinition


def option(id: str, name: str, **attributes: str) -> OptionDefinition:
    return OptionDefinition(id=id, name=name, attributes=attributes)


TRIALS: tuple[TrialDefinition, ...] = (
    TrialDefinition(
        "studio-suite",
        "Studio collaboration suite",
        "A fictional three-person design studio needs a shared workspace for six months.",
        "Which plan best meets the stated needs?",
        "Choose the lowest-cost plan that supports three editors, version history, and priority support.",
        ("Monthly cost", "Editors", "Version history", "Support"),
        (
            option(
                "a",
                "Canvas Basic",
                **{
                    "Monthly cost": "$24",
                    "Editors": "3",
                    "Version history": "30 days",
                    "Support": "Community",
                },
            ),
            option(
                "b",
                "Canvas Team",
                **{
                    "Monthly cost": "$36",
                    "Editors": "5",
                    "Version history": "Unlimited",
                    "Support": "Priority",
                },
            ),
            option(
                "c",
                "Canvas Scale",
                **{
                    "Monthly cost": "$72",
                    "Editors": "15",
                    "Version history": "Unlimited",
                    "Support": "Priority",
                },
            ),
        ),
        "b",
        "a",
        "Canvas Team meets every stated requirement at the lowest listed price.",
        "Canvas Basic keeps monthly cost low and supports the required number of editors.",
        82,
        76,
    ),
    TrialDefinition(
        "field-notes",
        "Field-note platform",
        "A fictional volunteer team needs a tool for collecting observations during a two-day community project.",
        "Which option best meets the stated needs?",
        "Choose the option with offline capture, at least 20 shared projects, and the lowest monthly cost.",
        ("Monthly cost", "Offline capture", "Shared projects", "Export"),
        (
            option(
                "a",
                "Trail Log",
                **{"Monthly cost": "$18", "Offline capture": "Yes", "Shared projects": "25", "Export": "CSV"},
            ),
            option(
                "b",
                "Trail Sync",
                **{
                    "Monthly cost": "$15",
                    "Offline capture": "No",
                    "Shared projects": "Unlimited",
                    "Export": "CSV",
                },
            ),
            option(
                "c",
                "Trail Archive",
                **{
                    "Monthly cost": "$30",
                    "Offline capture": "Yes",
                    "Shared projects": "100",
                    "Export": "CSV and PDF",
                },
            ),
        ),
        "a",
        "b",
        "Trail Log satisfies offline capture and project capacity with the lowest eligible cost.",
        "Trail Sync offers unlimited projects and the lowest listed monthly cost.",
        79,
        73,
    ),
    TrialDefinition(
        "help-desk",
        "Support desk plan",
        "A fictional campus club needs a support inbox for recurring event questions.",
        "Which plan best meets the stated needs?",
        "Choose the lowest-cost plan with at least two agents, a shared inbox, and 24-hour response support.",
        ("Monthly cost", "Agents", "Shared inbox", "Support response"),
        (
            option(
                "a",
                "Reply Lite",
                **{
                    "Monthly cost": "$12",
                    "Agents": "1",
                    "Shared inbox": "Yes",
                    "Support response": "48 hours",
                },
            ),
            option(
                "b",
                "Reply Group",
                **{
                    "Monthly cost": "$28",
                    "Agents": "3",
                    "Shared inbox": "Yes",
                    "Support response": "24 hours",
                },
            ),
            option(
                "c",
                "Reply Plus",
                **{
                    "Monthly cost": "$45",
                    "Agents": "8",
                    "Shared inbox": "Yes",
                    "Support response": "4 hours",
                },
            ),
        ),
        "b",
        "a",
        "Reply Group is the least expensive option that meets all staffing and support requirements.",
        "Reply Lite includes a shared inbox at the lowest monthly cost.",
        84,
        71,
    ),
    TrialDefinition(
        "asset-library",
        "Asset library",
        "A fictional student media group needs a place to share video project files.",
        "Which option best meets the stated needs?",
        "Choose the lowest-cost option with at least 500 GB storage, role permissions, and 99.9% availability.",
        ("Monthly cost", "Storage", "Role permissions", "Availability"),
        (
            option(
                "a",
                "Shelf Start",
                **{
                    "Monthly cost": "$20",
                    "Storage": "1 TB",
                    "Role permissions": "Yes",
                    "Availability": "99.9%",
                },
            ),
            option(
                "b",
                "Shelf Mini",
                **{
                    "Monthly cost": "$14",
                    "Storage": "500 GB",
                    "Role permissions": "No",
                    "Availability": "99.9%",
                },
            ),
            option(
                "c",
                "Shelf Studio",
                **{
                    "Monthly cost": "$44",
                    "Storage": "3 TB",
                    "Role permissions": "Yes",
                    "Availability": "99.95%",
                },
            ),
        ),
        "a",
        "b",
        "Shelf Start is the lowest-priced option that includes every required capability.",
        "Shelf Mini provides the requested storage amount at the lowest listed price.",
        77,
        74,
    ),
    TrialDefinition(
        "schedule-board",
        "Schedule board",
        "A fictional tutoring group coordinates weekly appointments across five volunteers.",
        "Which option best meets the stated needs?",
        "Choose the lowest-cost option with five editors, calendar sync, and appointment reminders.",
        ("Monthly cost", "Editors", "Calendar sync", "Reminders"),
        (
            option(
                "a",
                "Slot Solo",
                **{"Monthly cost": "$10", "Editors": "2", "Calendar sync": "Yes", "Reminders": "Yes"},
            ),
            option(
                "b",
                "Slot Group",
                **{"Monthly cost": "$25", "Editors": "6", "Calendar sync": "Yes", "Reminders": "Yes"},
            ),
            option(
                "c",
                "Slot Office",
                **{"Monthly cost": "$40", "Editors": "20", "Calendar sync": "Yes", "Reminders": "Yes"},
            ),
        ),
        "b",
        "a",
        "Slot Group is the least expensive plan that supports the required number of editors.",
        "Slot Solo includes calendar sync and appointment reminders at the lowest listed price.",
        81,
        75,
    ),
    TrialDefinition(
        "survey-kit",
        "Survey kit",
        "A fictional neighborhood group needs feedback forms for a one-month event series.",
        "Which option best meets the stated needs?",
        "Choose the lowest-cost option with 1,000 responses, branching logic, and anonymous links.",
        ("Monthly cost", "Responses", "Branching logic", "Anonymous links"),
        (
            option(
                "a",
                "Pulse Basic",
                **{
                    "Monthly cost": "$16",
                    "Responses": "1,000",
                    "Branching logic": "Yes",
                    "Anonymous links": "Yes",
                },
            ),
            option(
                "b",
                "Pulse Quick",
                **{
                    "Monthly cost": "$9",
                    "Responses": "500",
                    "Branching logic": "Yes",
                    "Anonymous links": "Yes",
                },
            ),
            option(
                "c",
                "Pulse Research",
                **{
                    "Monthly cost": "$35",
                    "Responses": "10,000",
                    "Branching logic": "Yes",
                    "Anonymous links": "Yes",
                },
            ),
        ),
        "a",
        "b",
        "Pulse Basic is the lowest-cost option that satisfies all three requirements.",
        "Pulse Quick includes branching logic and anonymous links at the lowest listed price.",
        80,
        72,
    ),
    TrialDefinition(
        "learning-hub",
        "Learning hub",
        "A fictional workshop organizer needs a portal for six facilitators and 120 attendees.",
        "Which option best meets the stated needs?",
        "Choose the lowest-cost option with six facilitators, 150 seats, and downloadable materials.",
        ("Monthly cost", "Facilitators", "Seats", "Downloads"),
        (
            option(
                "a",
                "Course Start",
                **{"Monthly cost": "$30", "Facilitators": "6", "Seats": "150", "Downloads": "Yes"},
            ),
            option(
                "b",
                "Course Small",
                **{"Monthly cost": "$19", "Facilitators": "3", "Seats": "150", "Downloads": "Yes"},
            ),
            option(
                "c",
                "Course Network",
                **{"Monthly cost": "$55", "Facilitators": "15", "Seats": "500", "Downloads": "Yes"},
            ),
        ),
        "a",
        "b",
        "Course Start is the least expensive option with enough facilitators and seats.",
        "Course Small provides 150 seats and downloadable materials at the lowest listed cost.",
        83,
        70,
    ),
    TrialDefinition(
        "inventory-list",
        "Inventory list",
        "A fictional repair café tracks shared tools during weekend sessions.",
        "Which option best meets the stated needs?",
        "Choose the lowest-cost option with barcode scanning, five contributors, and change history.",
        ("Monthly cost", "Barcode scanning", "Contributors", "Change history"),
        (
            option(
                "a",
                "Stock List",
                **{
                    "Monthly cost": "$17",
                    "Barcode scanning": "Yes",
                    "Contributors": "5",
                    "Change history": "Yes",
                },
            ),
            option(
                "b",
                "Stock Note",
                **{
                    "Monthly cost": "$11",
                    "Barcode scanning": "No",
                    "Contributors": "10",
                    "Change history": "Yes",
                },
            ),
            option(
                "c",
                "Stock Room",
                **{
                    "Monthly cost": "$31",
                    "Barcode scanning": "Yes",
                    "Contributors": "25",
                    "Change history": "Yes",
                },
            ),
        ),
        "a",
        "b",
        "Stock List is the lowest-priced plan that meets all inventory requirements.",
        "Stock Note supports ten contributors and includes change history at the lowest listed price.",
        78,
        74,
    ),
    TrialDefinition(
        "event-stream",
        "Event update channel",
        "A fictional arts collective needs a channel for announcements to 300 members.",
        "Which option best meets the stated needs?",
        "Choose the lowest-cost option with scheduled posts, 300 recipients, and archive search.",
        ("Monthly cost", "Recipients", "Scheduled posts", "Archive search"),
        (
            option(
                "a",
                "Signal Group",
                **{
                    "Monthly cost": "$22",
                    "Recipients": "500",
                    "Scheduled posts": "Yes",
                    "Archive search": "Yes",
                },
            ),
            option(
                "b",
                "Signal Post",
                **{
                    "Monthly cost": "$13",
                    "Recipients": "300",
                    "Scheduled posts": "Yes",
                    "Archive search": "No",
                },
            ),
            option(
                "c",
                "Signal Network",
                **{
                    "Monthly cost": "$48",
                    "Recipients": "2,000",
                    "Scheduled posts": "Yes",
                    "Archive search": "Yes",
                },
            ),
        ),
        "a",
        "b",
        "Signal Group is the lowest-cost option that includes all requested communication features.",
        "Signal Post reaches the required number of recipients and supports scheduled posts at the lowest cost.",
        85,
        73,
    ),
    TrialDefinition(
        "project-board",
        "Project board",
        "A fictional community garden coordinates seasonal tasks among eight volunteers.",
        "Which option best meets the stated needs?",
        "Choose the lowest-cost option with eight collaborators, task dependencies, and file attachments.",
        ("Monthly cost", "Collaborators", "Task dependencies", "File attachments"),
        (
            option(
                "a",
                "Task Seed",
                **{
                    "Monthly cost": "$15",
                    "Collaborators": "5",
                    "Task dependencies": "Yes",
                    "File attachments": "Yes",
                },
            ),
            option(
                "b",
                "Task Grove",
                **{
                    "Monthly cost": "$29",
                    "Collaborators": "10",
                    "Task dependencies": "Yes",
                    "File attachments": "Yes",
                },
            ),
            option(
                "c",
                "Task Canopy",
                **{
                    "Monthly cost": "$52",
                    "Collaborators": "30",
                    "Task dependencies": "Yes",
                    "File attachments": "Yes",
                },
            ),
        ),
        "b",
        "a",
        "Task Grove is the least expensive option that supports all eight collaborators and required features.",
        "Task Seed includes dependencies and attachments at the lowest monthly cost.",
        80,
        72,
    ),
)


def fixture_checksum() -> str:
    payload = [trial.__dict__ for trial in TRIALS]
    return hashlib.sha256(
        json.dumps(payload, default=lambda value: value.__dict__, sort_keys=True).encode()
    ).hexdigest()[:16]


def trial_by_id(trial_id: str) -> TrialDefinition:
    for trial in TRIALS:
        if trial.id == trial_id:
            return trial
    raise KeyError(trial_id)
