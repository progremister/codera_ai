import Head from "next/head";

const LandingLayout = ({ children }: { children: React.ReactNode }) => {
  return (
    <>
      <Head>
        <link rel="icon" href="/favicons/favicon.ico" />
        <link
          rel="icon"
          href="favicons/favicon-32x32.png"
          type="image/png"
          sizes="32x32"
        />
        <link
          rel="icon"
          href="/favicons/favicon-16x16.png"
          type="image/png"
          sizes="16x16"
        />
      </Head>
      <main className="h-full bg-[#111827] overflow-auto">
        <div className="mx-auto max-w-screen-xl h-full w-full">{children}</div>
      </main>
    </>
  );
};

export default LandingLayout;
