"""Build actual course-framework objects and generate annotated Mermaid views."""
from pathlib import Path
import argparse
import copy
import html
import textwrap
from goalmodeling.schema import (AchieveGoal, MaintainGoal, AvoidGoal, SoftGoal,
    Agent, AgentType, PerformanceLink, Refinement, ConflictLink,
    generate_graph, generate_pako_link)
from goal_catalog import (GOALS, TEO, ANGELA, ROB, ALIASES, MERGED_TEXT,
    COMBINED_EXTRA, CONFLICTS)

HERE = Path(__file__).resolve().parent
KINDS = {'Achieve':AchieveGoal, 'Maintain':MaintainGoal, 'Avoid':AvoidGoal, 'Soft':SoftGoal}


def canonical(gid):
    return ALIASES.get(gid, gid)


def specifications(name):
    if name == 'combined':
        goals = {k:copy.deepcopy(v) for k,v in GOALS.items() if k not in ALIASES}
        for old,new in ALIASES.items():
            goals[new]['evidence'] = sorted(set(goals[new]['evidence'] + GOALS[old]['evidence']))
            goals[new]['text'] = MERGED_TEXT[new]
        relations = []
        for parent,children,code,complete in TEO+ANGELA+ROB+COMBINED_EXTRA:
            parent = canonical(f'G-{parent}')
            children = list(dict.fromkeys(canonical(f'G-{n}') for n in children))
            children = [c for c in children if c != parent]
            relations.append((parent,children,code,complete))
        # Complementary refinements must form one AND group, not separate OR
        # alternatives. Only G-11 intentionally has alternative refinements.
        for parent,code in [('G-3','H5'),('G-23','H5'),('G-38','P4')]:
            children = [c for p,cs,_,_ in relations if p==parent for c in cs]
            relations = [r for r in relations if r[0]!=parent]
            relations.append((parent,list(dict.fromkeys(children)),code,False))
        return goals, relations, ['G-71'], CONFLICTS
    stakeholder = name.capitalize()
    goals = {k:copy.deepcopy(v) for k,v in GOALS.items() if v['stakeholder']==stakeholder}
    # Individual models retain their own source perspective, including local
    # inferred goals. The combined-only assumptions are not silently backfilled.
    relations = {'Teo':TEO,'Angela':ANGELA,'Rob':ROB}[stakeholder]
    relations = [(f'G-{p}',[f'G-{c}' for c in cs],code,full) for p,cs,code,full in relations]
    roots = {'Teo':['G-1','G-2','G-23'], 'Angela':['G-25','G-43','G-45'], 'Rob':['G-46']}[stakeholder]
    return goals, relations, roots, []


def build_model(name='combined'):
    specs, relations, roots, conflicts = specifications(name)
    parents = {r[0] for r in relations}
    agents = {}
    goals = {}
    for gid,s in specs.items():
        agent = s['agent']
        if agent and agent not in agents:
            agents[agent] = Agent(agent, AgentType.SOFTWARE_AGENT if agent=='Maintenance system' else AgentType.ENVIRONMENT_AGENT)
        label = f"{gid} {s['text']}"
        label = '<br/>'.join(html.escape(line) for line in textwrap.wrap(label, 48))
        annotation = s['category']
        if s['inferred']:
            annotation += '; interpretation beyond transcript'
        goals[gid] = KINDS[s['kind']](label, leaf=gid not in parents,
            annotation=annotation,
            performs=[PerformanceLink(agents[agent],None)] if agent else None)
    for p,cs,code,complete in relations:
        goals[p].disjunctions.append(Refinement(complete, [goals[c] for c in cs], annotation=code))
    links = [ConflictLink(goals[a],goals[b]) for a,b in conflicts]
    # Non-refined goals not reached from the named roots remain explicit roots.
    reached = set()
    def visit(gid):
        if gid in reached: return
        reached.add(gid)
        for p,cs,_,_ in relations:
            if p==gid:
                for c in cs: visit(c)
    for r in roots: visit(r)
    roots = roots + [k for k in goals if k not in reached]
    return {'goals':goals,'specs':specs,'relations':relations,'roots':roots,'links':links}


def diagram(model):
    result = generate_graph([model['goals'][k] for k in model['roots']],model['links'])
    result += '\n%% Yellow = added interpretation; functional/category labels are annotations.\n'
    for gid,s in model['specs'].items():
        if model['goals'][gid].leaf:
            result += f"class {model['goals'][gid].get_node_id()} bold\n"
        if s['inferred']:
            result += f"style {model['goals'][gid].get_node_id()} fill:#fff59d,color:#111\n"
    return result


def export_model(name, output_dir=None):
    out = Path(output_dir or HERE/'generated')
    out.mkdir(parents=True,exist_ok=True)
    model = build_model(name)
    code = diagram(model)
    config = {'theme':'neutral','securityLevel':'strict',
        'flowchart':{'htmlLabels':True,'curve':'linear','nodeSpacing':35,'rankSpacing':60},
        'themeVariables':{'fontFamily':'Arial','fontSize':'15px'}}
    # More generous maxTextSize is required for the combined, evidence-rich graph.
    config['maxTextSize'] = 200000
    link = generate_pako_link(code,'view',config=config)
    (out/f'goal_model_{name}.mmd').write_text(code,encoding='utf-8')
    (out/f'goal_model_{name}_link.txt').write_text(link+'\n',encoding='utf-8')
    if name=='combined': (HERE/'mermaid.txt').write_text(link+'\n',encoding='utf-8')
    return model,code,link


def main(name):
    parser=argparse.ArgumentParser(description=f'Generate the {name} goal model with the course goalmodeling framework.')
    parser.add_argument('--output-dir',type=Path)
    args=parser.parse_args()
    model,code,link=export_model(name,args.output_dir)
    print(f"{name}: {len(model['goals'])} goals; Mermaid saved to {args.output_dir or HERE/'generated'}")
    print(link)
