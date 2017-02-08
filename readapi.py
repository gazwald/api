#!/usr/bin/env python3

from myapi import ContactRequest

for result in ContactRequest.query.all():
    header = "{name} ({email}) attempted to contact you on {date}, message:"
    print(header.format(name=result.name,
                        email=result.email,
                        date=result.date,))
    print(result.message)
