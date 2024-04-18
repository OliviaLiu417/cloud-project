import Image from "next/image";
import styles from "./page.module.css";
import Footer from "./components/Footer";
import Header from "./components/Header";
import Content from "./components/Content";
import { Suspense } from "react";

export default function Home() {
  return (
    <main className={styles.main}>
      <div className={styles.contentContainer}>
        <Suspense>
          <Header />
        </Suspense>
        <div className={styles.container}>
          <Suspense>
            <Content />
          </Suspense>
        </div>
      </div>
      <Footer />
    </main>
  );
}
