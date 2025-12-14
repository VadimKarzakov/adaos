from adaos.sdk.data import ctx_subnet


def test_ctx_subnet_noop_context_manager():
    # Should act as a no-op context manager for legacy skills.
    with ctx_subnet("demo"):
        pass
