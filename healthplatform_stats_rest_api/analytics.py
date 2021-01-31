from codecs import decode, encode
from os import environ

import pandas as pd
from sqlalchemy import create_engine


def get_stats():
    def as_query(alias_username):
        return " ".join(
            (
                "{alias} AS (".format(alias=alias_username[0]),
                'SELECT "artifactLocation",\n',
                '        category as "category_{alias}"\n'.format(
                    alias=alias_username[0]
                ),
                "        FROM categorise_tbl\n",
                "        WHERE username = '{username}')".format(
                    username=alias_username[1]
                ),
            )
        )

    def next_query(alias_username):
        return "category_{alias}".format(alias=alias_username[0])

    def natural_join(alias_username):
        return "NATURAL JOIN {alias}".format(alias=alias_username[0])

    engine = create_engine(environ["RDBMS_URI"])
    usernames = (
        pd.read_sql("SELECT DISTINCT username " "FROM categorise_tbl", engine)
        .set_index("username")
        .index
    )

    username2alias = {
        encode("nqevnashatv@lnubb.pbz.nh", "rot13"): "ret",
        decode("unzb.qj@tznvy.pbz", "rot13"): "oph",
        encode("uryra.athlra1@hafj.rqh.nh", "rot13"): "pro",
    }
    idx_username = tuple(
        map(
            lambda idx_username: (
                username2alias.get(
                    idx_username[1], "q{c:02d}".format(c=idx_username[0])
                ),
                idx_username[1],
            ),
            enumerate(usernames),
        )
    )
    fst = idx_username[0][0]
    sql = "".join(
        (
            "WITH ",
            ",\n".join(map(as_query, idx_username)),
            '\n\nSELECT {fst}."artifactLocation",'.format(fst=fst),
            "\n       category_{fst},".format(fst=fst),
            "\n       ",
            ",\n       ".join(map(next_query, idx_username[1:])),
            "\nFROM {fst}\n".format(fst=fst),
            "\n".join(map(natural_join, idx_username[1:])),
            ";",
        )
    )

    df = pd.read_sql(sql, engine).set_index("artifactLocation")

    return df.apply(pd.value_counts).to_dict()
