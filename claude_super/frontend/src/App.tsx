import Header from "./components/Header";

export default function App() {
  return (
    <div className="flex h-full flex-col bg-neutral-0 font-sans text-neutral-900 dark:bg-neutral-900 dark:text-neutral-50">
      <Header onMenuClick={() => {}} />
      <main className="flex-1" />
    </div>
  );
}
