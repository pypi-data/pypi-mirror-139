from . import tmux


class Context:
    def __init__(self, manager, pane, parent, **environ):
        self.manager = manager
        self.pane = pane
        self.parent = parent
        self.environ = environ
        self.previous = None
        self.echo = True

    @property
    def lineage(self):
        return f'{self.parent.lineage}.{self.name}' if self.parent else self.name

    def do_enter(self):
        raise NotImplemented

    def run(self, cmd, **kw):
        head = kw.get(
            'head',
            f' -> {cmd}' if self.echo else None
        )
        prompt = kw.get('exp', self.prompt)
        self.pane.run(cmd, exp=prompt, head=head, **kw)

    def enter(self):
        current = self.manager.current
        print(f' + {self.name}')
        bak, self.echo = self.echo, False
        self.do_enter()
        self.pane.prompt = self.prompt
        self.echo = bak
        self.previous = current
        self.manager.current = self

    def exit_cmd(self):
        self.pane.send_keys('C-d')

    def wait_cmd(self, what):
        self.pane.wait(what)

    def exit(self):
        print(f' - {self.name}')
        self.exit_cmd()
        if self.previous:
            self.wait_cmd(self.previous.prompt)
            self.manager.current = self.previous
            self.pane.prompt = self.previous.prompt

    def __str__(self):
        return self.lineage


class Root(Context):
    name = None
    prompt = r'.*\$$'
    def do_enter(self): pass
    def exit_cmd(self): pass
    def exit(self): pass
    def __bool__(self):
        return False


class Manager:
    def __init__(self, pane, ctxs, **kw):
        prompt = kw.pop('prompt', None)
        if prompt:
            Root.prompt = prompt
        self.current = Root(
            self,
            pane,
            None,
        )

        cdict = {None : self.current}
        for ctx in ctxs:
            cdict[ctx.name] = ctx(
                self,
                pane,
                cdict.get(ctx.parent),
                **kw
            )
        self.contexts = cdict

    def enter(self, target):
        last = self.current

        target = self.contexts[target]
        targets = target.lineage.split('.')

        while self.current and self.current.name not in targets:
            self.current.exit()

        for name in targets:
            names = self.current.lineage.split('.') if self.current else []
            if name not in names:
                ctx = self.contexts[name]
                ctx.enter()

        if self.current != last:
            print(f' = {self.current}')

    def exit(self, target=None):
        last = self.current

        if not target:
            target = self.current.previous.name

        while self.current.name!=target:
            self.current.exit()
            if not self.current.parent:
                self.current.exit()
                break

        if self.current != last:
            print(f' = {self.current}')

    def __getattr__(self, attr):
        return getattr(self.current.pane, attr)


class MultiPanes:
    # mandatory seq of Context's subclass
    contexts = list()

    # optional arbitrary data transfered to contexts
    environ = dict()

    # space speparated panes's names
    panes = ''

    def __init__(self):
        assert self.contexts
        assert all(
            issubclass(ctx, Context)
            for ctx in self.contexts
        )
        self.__dict__.update(self.environ)
        self.names = {
            name : idx
            for idx, name in enumerate(self.panes.split())
        }
        assert len(names)>1

        session = tmux.active
        self.win = session.new()
        self.cur = self.win.left

        manager = Manager(
            self.cur,
            self.contexts,
            **self.environ
        )
        self.managers = [manager]
        self.current = manager

        for n in list(self.names)[1:]:
            self.add()
            self.win.even()

    def add(self):
        self.cur = self.win.right
        self.win.split()
        self.cur = self.win.right
        manager = Manager(
            self.cur,
            self.contexts,
            **self.environ
        )
        self.managers.append(manager)
        self.current = manager

    def select(self, name):
        idx = self.names[name]
        self.current = self.managers[idx]
        self.win.select(idx)

    @property
    def width(self):
        return self.current.current.pane.width

    @width.setter
    def width(self, percent):
        self.current.current.pane.width = percent

    def __getattr__(self, attr):
        try:
            return getattr(self.current, attr)
        except Exception as x:
            print(f'\n ! getattr {attr} ! {x}\n')
            raise

