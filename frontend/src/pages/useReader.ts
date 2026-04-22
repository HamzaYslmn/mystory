import { useCallback, useEffect, useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getProgress, useProgressStore } from '@/store/progress';
import { getBookBySlug, getPageContent, type Book, type Page } from '@/utils/markdown';

// MARK: - useReader: encapsulates book/page resolution + nav
export function useReader(bookSlug: string | undefined, pageSlug: string | undefined) {
  const navigate = useNavigate();
  const setProgress = useProgressStore((s) => s.set);
  const clearProgress = useProgressStore((s) => s.clear);

  const book = useMemo<Book | null>(
    () => (bookSlug ? getBookBySlug(bookSlug) : null),
    [bookSlug],
  );

  // MARK: - Resolve current page entry (falls back to saved progress, then 0)
  const { entry, pageIndex, total, hasPrev, hasNext } = useMemo(() => {
    if (!book) return { entry: null, pageIndex: -1, total: 0, hasPrev: false, hasNext: false };
    const target = pageSlug || getProgress(book.bookSlug) || '';
    const i = Math.max(0, book.pages.findIndex((p) => p.pageSlug === target));
    const t = book.pages.length;
    return {
      entry: book.pages[i] ?? null,
      pageIndex: i,
      total: t,
      hasPrev: i > 0,
      hasNext: i < t - 1,
    };
  }, [book, pageSlug]);

  // MARK: - Single effect: redirect, persist progress, scroll-to-top, load page
  const [page, setPage] = useState<Page | null>(null);
  useEffect(() => {
    if (!bookSlug) return;
    if (!book) { navigate('/', { replace: true }); return; }
    if (!entry) return;
    if (pageSlug !== entry.pageSlug) {
      navigate(`/reader/${book.bookSlug}/${entry.pageSlug}`, { replace: true });
      return;
    }
    setProgress(book.bookSlug, entry.pageSlug);
    window.scrollTo({ top: 0, behavior: 'auto' });
    setPage(null);
    let alive = true;
    getPageContent(book.bookSlug, entry.pageSlug).then((p) => alive && setPage(p));
    return () => { alive = false; };
  }, [bookSlug, book, entry, pageSlug, navigate, setProgress]);

  // MARK: - Navigation helpers
  const goTo = useCallback((i: number) => {
    if (!book || i < 0 || i >= book.pages.length) return;
    navigate(`/reader/${book.bookSlug}/${book.pages[i].pageSlug}`);
  }, [book, navigate]);

  const goPrev = useCallback(() => goTo(pageIndex - 1), [goTo, pageIndex]);
  const goNext = useCallback(() => goTo(pageIndex + 1), [goTo, pageIndex]);
  const finish = useCallback(() => { if (book) clearProgress(book.bookSlug); }, [book, clearProgress]);

  return { book, entry, page, pageIndex, total, hasPrev, hasNext, goPrev, goNext, finish };
}
