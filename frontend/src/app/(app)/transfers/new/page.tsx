import { TransferForm } from "@/components/TransferForm";

export default function NewTransferPage() {
  return (
    <div className="space-y-4">
      <h1 className="text-xl font-bold">New ownership transfer</h1>
      <TransferForm transfer={null} />
    </div>
  );
}
