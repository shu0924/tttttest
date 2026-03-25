import sys
sys.path.append('..')
import lib.rel_algebra_calculus.rel_algebra_calculus as ra

def queries(univDB):
    tables = univDB["tables"]
    department = tables["department"]
    course = tables["course"]
    prereq = tables["prereq"]
    class_ = tables["class"]
    faculty = tables["faculty"]
    student = tables["student"]
    enrollment = tables["enrollment"]
    transcript = tables["transcript"]
    # Query 1: CS students who received at least one A
    query1 = ra.distinct(
        ra.proj(
            ra.join(
                ra.sel(
                    student,
                    lambda s:s["major"] == "CS"),
                ra.sel(
                    transcript,
                    lambda t:t["grade"] == "A")
            ),
            ["ssn", "name", "major", "status"]   
        )
    )

    # Query 2: CS students who received A in at least two different courses
    query2 = ra.distinct(
        ra.proj(
            ra.join(
                ra.sel(student, lambda s: s["major"] == "CS"),
                ra.sel(
                    ra.join(
                        ra.ren(
                            ra.sel(transcript, lambda t: t["grade"] == "A"),
                            {"dcode": "dcode1", "cno": "cno1", "grade": "grade1"}
                        ),
                        ra.sel(transcript, lambda t: t["grade"] == "A")
                    ),
                    lambda pair: pair["ssn"] == pair["ssn"] and (
                        pair["dcode1"] != pair["dcode"] or pair["cno1"] != pair["cno"]
                    )
                )
            ),
            ["ssn", "name", "major", "status"]
        )
    )


    # Query 3: CS students who only got A in all CS courses they took
    # Query 3: CS students who got A in all CS courses they have taken (using division logic)
    query3 = ra.distinct(
        ra.proj(
            ra.diff(
                ra.sel(student, lambda s: s["major"] == "CS"),
                ra.proj(
                    ra.join(
                        ra.sel(student, lambda s: s["major"] == "CS"),
                        ra.sel(transcript, lambda t: t["dcode"] == "CS" and t["grade"] != "A")
                    ),
                    ["ssn", "name", "major", "status"]
                )
            ),
            ["ssn", "name", "major", "status"]
        )
    )



    ra.sortTable(query1,["ssn"])
    ra.sortTable(query2,["ssn"])
    ra.sortTable(query3, ['ssn'])

    return {
        "query1": query1,
        "query2": query2,
        "query3": query3
    }
