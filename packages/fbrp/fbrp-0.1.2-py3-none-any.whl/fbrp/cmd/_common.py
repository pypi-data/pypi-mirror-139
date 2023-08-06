import fbrp.life_cycle
import fbrp.process


class CommonFlags:
    verbose = False


class autocomplete:
    @static
    def defined_processes(ctx, param, incomplete):
        return [
            proc
            for proc in fbrp.process.defined_processes
            if proc.startswith(incomplete)
        ]

    @static
    def running_processes(ctx, param, incomplete):
        state = fbrp.life_cycle.system_state().asdict()
        procs = state.get("procs", {}).keys()
        return [name for name, info in procs.items() if info.get("state") == "UP"]
