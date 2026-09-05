"""Rollen-Agenten als Plugins + Runner nach dem Playbook (PLAN.md §7).

    registry = RoleRegistry(roles_dir)        # liest roles/<name>/role.yaml, ROLE.md, criteria.md, prompt.md
    runner = AgentRunner(registry, llm, retrieval_client, escalations, perms)
    assessment = runner.run_role("cfo", project, ctx)     -> mpb.types.Assessment

Importiert mpb.knowledge NICHT. Bekommt einen RetrievalClient injiziert (Konzept §2.8).
"""
