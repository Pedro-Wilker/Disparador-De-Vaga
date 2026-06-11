import Link from "next/link";

export default function Home() {
  return (
    <div className="flex flex-col flex-1 items-center justify-center bg-zinc-50 font-sans dark:bg-black min-h-screen">
      <main className="flex w-full max-w-2xl flex-col items-center justify-center py-20 px-8 gap-8 bg-white dark:bg-zinc-900 rounded-3xl border border-zinc-200 dark:border-zinc-800 shadow-sm">
        
        <div className="text-center space-y-4">
          <h1 className="text-4xl font-bold tracking-tight text-black dark:text-zinc-50">
            JobPilot
          </h1>
          <p className="text-lg text-zinc-600 dark:text-zinc-400">
            Gerencie suas candidaturas de forma inteligente.
          </p>
        </div>

        <div className="flex flex-col w-full max-w-xs gap-4">
          <Link
            href="/login"
            className="flex h-12 w-full items-center justify-center rounded-full bg-indigo-600 px-5 text-white transition-colors hover:bg-indigo-700 font-medium"
          >
            Entrar
          </Link>
          
          <Link
            href="/register"
            className="flex h-12 w-full items-center justify-center rounded-full border border-solid border-zinc-300 dark:border-zinc-700 px-5 text-zinc-900 dark:text-white transition-colors hover:bg-zinc-100 dark:hover:bg-zinc-800 font-medium"
          >
            Criar conta
          </Link>
        </div>

      </main>
    </div>
  );
}