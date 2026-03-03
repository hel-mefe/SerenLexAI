import { AuthHeader } from "./AuthHeader"
import { SignInForm } from "./SignInForm"
import { AuthFooter } from "./AuthFooter"

export function AuthPanel() {
  return (
    <div className="flex-1 flex flex-col bg-white border-none rounded-4xl">
      <AuthHeader />
      <SignInForm />
      <AuthFooter />
    </div>
  )
}