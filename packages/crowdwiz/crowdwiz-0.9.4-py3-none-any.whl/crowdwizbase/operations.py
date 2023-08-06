# -*- coding: utf-8 -*-
import json

from collections import OrderedDict
from binascii import hexlify, unhexlify

from graphenebase.types import (
	Array,
	Bool,
	Bytes,
	Fixed_array,
	Id,
	Int16,
	Int64,
	Map,
	Optional,
	PointInTime,
	Set,
	Signature,
	Static_variant,
	String,
	Uint8,
	Uint16,
	Uint32,
	Uint64,
	Varint32,
	Void,
	VoteId,
	Ripemd160,
	Sha1,
	Sha256,
)

from .account import PublicKey
from .objects import (
	AccountCreateExtensions,
	AccountOptions,
	Asset,
	AssetOptions,
	BitAssetOptions,
	CallOrderExtension,
	GrapheneObject,
	Memo,
	ObjectId,
	Operation,
	Permission,
	Price,
	PriceFeed,
	SpecialAuthority,
	Worker_initializer,
	isArgsThisClass,
	Policy,
	Policy1
)
from .operationids import operations


default_prefix = "CWD"
class_idmap = {}
class_namemap = {}


def fill_classmaps():
	for name, ind in operations.items():
		classname = name[0:1].upper() + name[1:]
		class_namemap[classname] = ind
		try:
			class_idmap[ind] = globals()[classname]
		except Exception:
			continue


def getOperationClassForId(op_id):
	""" Convert an operation id into the corresponding class
	"""
	return class_idmap[op_id] if op_id in class_idmap else None


def getOperationIdForClass(name):
	""" Convert an operation classname into the corresponding id
	"""
	return class_namemap[name] if name in class_namemap else None


def getOperationNameForId(i):
	""" Convert an operation id into the corresponding string
	"""
	for key in operations:
		if int(operations[key]) is int(i):
			return key
	return "Unknown Operation ID %d" % i


class Transfer(GrapheneObject):
	def __init__(self, *args, **kwargs):
		# Allow for overwrite of prefix
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			prefix = kwargs.get("prefix", default_prefix)
			if "memo" in kwargs and kwargs["memo"]:
				if isinstance(kwargs["memo"], dict):
					kwargs["memo"]["prefix"] = prefix
					memo = Optional(Memo(**kwargs["memo"]))
				else:
					memo = Optional(Memo(kwargs["memo"]))
			else:
				memo = Optional(None)
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("from", ObjectId(kwargs["from"], "account")),
						("to", ObjectId(kwargs["to"], "account")),
						("amount", Asset(kwargs["amount"])),
						("memo", memo),
						("extensions", Set([])),
					]
				)
			)


class Asset_publish_feed(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("publisher", ObjectId(kwargs["publisher"], "account")),
						("asset_id", ObjectId(kwargs["asset_id"], "asset")),
						("feed", PriceFeed(kwargs["feed"])),
						("extensions", Set([])),
					]
				)
			)


class Asset_create(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			if "bitasset_opts" in kwargs:
				bitasset_opts = Optional(BitAssetOptions(kwargs["bitasset_opts"]))
			else:
				bitasset_opts = Optional(None)
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("issuer", ObjectId(kwargs["issuer"], "account")),
						("symbol", String(kwargs["symbol"])),
						("precision", Uint8(kwargs["precision"])),
						("common_options", AssetOptions(kwargs["common_options"])),
						("bitasset_opts", bitasset_opts),
						(
							"is_prediction_market",
							Bool(bool(kwargs["is_prediction_market"])),
						),
						("extensions", Set([])),
					]
				)
			)


class Asset_update(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			if "new_issuer" in kwargs:
				raise ValueError(
					"Cannot change asset_issuer with Asset_update anylonger! (BSIP29)"
				)
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("issuer", ObjectId(kwargs["issuer"], "account")),
						(
							"asset_to_update",
							ObjectId(kwargs["asset_to_update"], "asset"),
						),
						("new_issuer", Optional(None)),
						("new_options", AssetOptions(kwargs["new_options"])),
						("extensions", Set([])),
					]
				)
			)


class Asset_update_bitasset(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("issuer", ObjectId(kwargs["issuer"], "account")),
						(
							"asset_to_update",
							ObjectId(kwargs["asset_to_update"], "asset"),
						),
						("new_options", BitAssetOptions(kwargs["new_options"])),
						("extensions", Set([])),
					]
				)
			)


class Asset_issue(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			prefix = kwargs.get("prefix", default_prefix)

			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			if "memo" in kwargs and kwargs["memo"]:
				memo = Optional(Memo(prefix=prefix, **kwargs["memo"]))
			else:
				memo = Optional(None)
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("issuer", ObjectId(kwargs["issuer"], "account")),
						("asset_to_issue", Asset(kwargs["asset_to_issue"])),
						(
							"issue_to_account",
							ObjectId(kwargs["issue_to_account"], "account"),
						),
						("memo", memo),
						("extensions", Set([])),
					]
				)
			)


class Op_wrapper(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			super().__init__(OrderedDict([("op", Operation(kwargs["op"]))]))


class Proposal_create(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			if "review_period_seconds" in kwargs:
				review = Optional(Uint32(kwargs["review_period_seconds"]))
			else:
				review = Optional(None)
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						(
							"fee_paying_account",
							ObjectId(kwargs["fee_paying_account"], "account"),
						),
						("expiration_time", PointInTime(kwargs["expiration_time"])),
						(
							"proposed_ops",
							Array([Op_wrapper(o) for o in kwargs["proposed_ops"]]),
						),
						("review_period_seconds", review),
						("extensions", Set([])),
					]
				)
			)


class Proposal_update(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]

			for o in [
				"active_approvals_to_add",
				"active_approvals_to_remove",
				"owner_approvals_to_add",
				"owner_approvals_to_remove",
				"key_approvals_to_add",
				"key_approvals_to_remove",
			]:
				if o not in kwargs:
					kwargs[o] = []

			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						(
							"fee_paying_account",
							ObjectId(kwargs["fee_paying_account"], "account"),
						),
						("proposal", ObjectId(kwargs["proposal"], "proposal")),
						(
							"active_approvals_to_add",
							Array(
								[
									ObjectId(o, "account")
									for o in kwargs["active_approvals_to_add"]
								]
							),
						),
						(
							"active_approvals_to_remove",
							Array(
								[
									ObjectId(o, "account")
									for o in kwargs["active_approvals_to_remove"]
								]
							),
						),
						(
							"owner_approvals_to_add",
							Array(
								[
									ObjectId(o, "account")
									for o in kwargs["owner_approvals_to_add"]
								]
							),
						),
						(
							"owner_approvals_to_remove",
							Array(
								[
									ObjectId(o, "account")
									for o in kwargs["owner_approvals_to_remove"]
								]
							),
						),
						(
							"key_approvals_to_add",
							Array(
								[PublicKey(o) for o in kwargs["key_approvals_to_add"]]
							),
						),
						(
							"key_approvals_to_remove",
							Array(
								[
									PublicKey(o)
									for o in kwargs["key_approvals_to_remove"]
								]
							),
						),
						("extensions", Set([])),
					]
				)
			)


class Limit_order_create(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("seller", ObjectId(kwargs["seller"], "account")),
						("amount_to_sell", Asset(kwargs["amount_to_sell"])),
						("min_to_receive", Asset(kwargs["min_to_receive"])),
						("expiration", PointInTime(kwargs["expiration"])),
						("fill_or_kill", Bool(kwargs["fill_or_kill"])),
						("extensions", Set([])),
					]
				)
			)


class Limit_order_cancel(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						(
							"fee_paying_account",
							ObjectId(kwargs["fee_paying_account"], "account"),
						),
						("order", ObjectId(kwargs["order"], "limit_order")),
						("extensions", Set([])),
					]
				)
			)


class Call_order_update(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						(
							"funding_account",
							ObjectId(kwargs["funding_account"], "account"),
						),
						("delta_collateral", Asset(kwargs["delta_collateral"])),
						("delta_debt", Asset(kwargs["delta_debt"])),
						("extensions", CallOrderExtension(kwargs["extensions"])),
					]
				)
			)


class Asset_fund_fee_pool(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("from_account", ObjectId(kwargs["from_account"], "account")),
						("asset_id", ObjectId(kwargs["asset_id"], "asset")),
						("amount", Int64(kwargs["amount"])),
						("extensions", Set([])),
					]
				)
			)


class Asset_claim_fees(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]

			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("issuer", ObjectId(kwargs["issuer"], "account")),
						("amount_to_claim", Asset(kwargs["amount_to_claim"])),
						("extensions", Set([])),
					]
				)
			)


class Asset_claim_pool(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]

			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("issuer", ObjectId(kwargs["issuer"], "account")),
						("asset_id", ObjectId(kwargs["asset_id"], "asset")),
						("amount_to_claim", Asset(kwargs["amount_to_claim"])),
						("extensions", Set([])),
					]
				)
			)


class Override_transfer(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			if "memo" in kwargs:
				memo = Optional(Memo(kwargs["memo"]))
			else:
				memo = Optional(None)
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("issuer", ObjectId(kwargs["issuer"], "account")),
						("from", ObjectId(kwargs["from"], "account")),
						("to", ObjectId(kwargs["to"], "account")),
						("amount", Asset(kwargs["amount"])),
						("memo", memo),
						("extensions", Set([])),
					]
				)
			)


class Account_create(GrapheneObject):
	def __init__(self, *args, **kwargs):
		# Allow for overwrite of prefix
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			prefix = kwargs.get("prefix", default_prefix)

			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("registrar", ObjectId(kwargs["registrar"], "account")),
						("referrer", ObjectId(kwargs["referrer"], "account")),
						("referrer_percent", Uint16(kwargs["referrer_percent"])),
						("name", String(kwargs["name"])),
						("owner", Permission(kwargs["owner"], prefix=prefix)),
						("active", Permission(kwargs["active"], prefix=prefix)),
						("options", AccountOptions(kwargs["options"], prefix=prefix)),
						("extensions", AccountCreateExtensions(kwargs["extensions"])),
					]
				)
			)


class Account_update(GrapheneObject):
	def __init__(self, *args, **kwargs):
		# Allow for overwrite of prefix
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			prefix = kwargs.get("prefix", default_prefix)

			if "owner" in kwargs:
				owner = Optional(Permission(kwargs["owner"], prefix=prefix))
			else:
				owner = Optional(None)

			if "active" in kwargs:
				active = Optional(Permission(kwargs["active"], prefix=prefix))
			else:
				active = Optional(None)

			if "new_options" in kwargs:
				options = Optional(AccountOptions(kwargs["new_options"], prefix=prefix))
			else:
				options = Optional(None)

			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("account", ObjectId(kwargs["account"], "account")),
						("owner", owner),
						("active", active),
						("new_options", options),
						("extensions", Set([])),
					]
				)
			)


class Account_whitelist(GrapheneObject):
	no_listing = 0  # < No opinion is specified about this account
	white_listed = 1  # < This account is whitelisted, but not blacklisted
	black_listed = 2  # < This account is blacklisted, but not whitelisted
	white_and_black_listed = 3  # < This account is both whitelisted and blacklisted

	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]

			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						(
							"authorizing_account",
							ObjectId(kwargs["authorizing_account"], "account"),
						),
						(
							"account_to_list",
							ObjectId(kwargs["account_to_list"], "account"),
						),
						("new_listing", Uint8(kwargs["new_listing"])),
						("extensions", Set([])),
					]
				)
			)


class Vesting_balance_withdraw(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]

			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						(
							"vesting_balance",
							ObjectId(kwargs["vesting_balance"], "vesting_balance"),
						),
						("owner", ObjectId(kwargs["owner"], "account")),
						("amount", Asset(kwargs["amount"])),
					]
				)
			)


class Account_upgrade(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						(
							"account_to_upgrade",
							ObjectId(kwargs["account_to_upgrade"], "account"),
						),
						(
							"upgrade_to_lifetime_member",
							Bool(kwargs["upgrade_to_lifetime_member"]),
						),
						("extensions", Set([])),
					]
				)
			)


class Witness_update(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			if "new_url" in kwargs and kwargs["new_url"]:
				new_url = Optional(String(kwargs["new_url"]))
			else:
				new_url = Optional(None)

			if "new_signing_key" in kwargs and kwargs["new_signing_key"]:
				new_signing_key = Optional(PublicKey(kwargs["new_signing_key"]))
			else:
				new_signing_key = Optional(None)

			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("witness", ObjectId(kwargs["witness"], "witness")),
						(
							"witness_account",
							ObjectId(kwargs["witness_account"], "account"),
						),
						("new_url", new_url),
						("new_signing_key", new_signing_key),
					]
				)
			)


class Asset_update_feed_producers(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]

			kwargs["new_feed_producers"] = sorted(
				kwargs["new_feed_producers"], key=lambda x: float(x.split(".")[2])
			)

			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("issuer", ObjectId(kwargs["issuer"], "account")),
						(
							"asset_to_update",
							ObjectId(kwargs["asset_to_update"], "asset"),
						),
						(
							"new_feed_producers",
							Array(
								[
									ObjectId(o, "account")
									for o in kwargs["new_feed_producers"]
								]
							),
						),
						("extensions", Set([])),
					]
				)
			)


class Asset_reserve(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]

			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("payer", ObjectId(kwargs["payer"], "account")),
						("amount_to_reserve", Asset(kwargs["amount_to_reserve"])),
						("extensions", Set([])),
					]
				)
			)


class Worker_create(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]

			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("owner", ObjectId(kwargs["owner"], "account")),
						("work_begin_date", PointInTime(kwargs["work_begin_date"])),
						("work_end_date", PointInTime(kwargs["work_end_date"])),
						("daily_pay", Uint64(kwargs["daily_pay"])),
						("name", String(kwargs["name"])),
						("url", String(kwargs["url"])),
						("initializer", Worker_initializer(kwargs["initializer"])),
					]
				)
			)


class Withdraw_permission_create(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						(
							"withdraw_from_account",
							ObjectId(kwargs["withdraw_from_account"], "account"),
						),
						(
							"authorized_account",
							ObjectId(kwargs["authorized_account"], "account"),
						),
						("withdrawal_limit", Asset(kwargs["withdrawal_limit"])),
						(
							"withdrawal_period_sec",
							Uint32(kwargs["withdrawal_period_sec"]),
						),
						(
							"periods_until_expiration",
							Uint32(kwargs["periods_until_expiration"]),
						),
						("period_start_time", PointInTime(kwargs["period_start_time"])),
						]
				)
			)


class Asset_global_settle(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]

			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("issuer", ObjectId(kwargs["issuer"], "account")),
						(
							"asset_to_settle",
							ObjectId(kwargs["asset_to_settle"], "asset"),
						),
						("settle_price", Price(kwargs["settle_price"])),
						("extensions", Set([])),
					]
				)
			)


class Committee_member_create(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						(
							"committee_member_account",
							ObjectId(kwargs["committee_member_account"], "account"),
						),
						("url", String(kwargs["url"])),
					]
				)
			)


class Custom(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("payer", ObjectId(kwargs["payer"], "account")),
						(
							"required_auths",
							Array(
								[
									ObjectId(o, "account")
									for o in kwargs["required_auths"]
								]
							),
						),
						("id", Uint16(kwargs["id"])),
						("data", Bytes(kwargs["data"])),
					]
				)
			)


class Bid_collateral(GrapheneObject):
	def detail(self, *args, **kwargs):
		# New pygraphene interface!
		return OrderedDict(
			[
				("fee", Asset(kwargs["fee"])),
				("bidder", ObjectId(kwargs["bidder"], "account")),
				("additional_collateral", Asset(kwargs["additional_collateral"])),
				("debt_covered", Asset(kwargs["debt_covered"])),
				("extensions", Set([])),
			]
		)


class Balance_claim(GrapheneObject):
	def detail(self, *args, **kwargs):
		# New pygraphene interface!
		prefix = kwargs.pop("prefix", default_prefix)
		return OrderedDict(
			[
				("fee", Asset(kwargs["fee"])),
				("deposit_to_account", ObjectId(kwargs["deposit_to_account"], "account")),
				("balance_to_claim", ObjectId(kwargs["balance_to_claim"], "balance")),
				("balance_owner_key", PublicKey(kwargs["balance_owner_key"], prefix=prefix)),
				("total_claimed", Asset(kwargs["total_claimed"])),
			]
		)


class Asset_settle(GrapheneObject):
	def detail(self, *args, **kwargs):
		# New pygraphene interface!
		return OrderedDict(
			[
				("fee", Asset(kwargs["fee"])),
				("account", ObjectId(kwargs["account"], "account")),
				("amount", Asset(kwargs["amount"])),
				("extensions", Set([])),
			]
		)


class Asset_update_issuer(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("issuer", ObjectId(kwargs["issuer"], "account")),
						(
							"asset_to_update",
							ObjectId(kwargs["asset_to_update"], "asset"),
						),
						("new_issuer", ObjectId(kwargs["new_issuer"], "account")),
						("extensions", Set([])),
					]
				)
			)


class Flipcoin_bet(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("bettor", ObjectId(kwargs["bettor"], "account")),
						("bet", Asset(kwargs["bet"])),
						("nonce", Uint8(kwargs["nonce"]))
					]
				)
			)


class Flipcoin_call(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("flipcoin", ObjectId(kwargs["flipcoin"], "flipcoin")),
						("caller", ObjectId(kwargs["caller"], "account")),
						("bet", Asset(kwargs["bet"])),
					]
				)
			)


class Lottery_goods_create_lot(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("owner", ObjectId(kwargs["owner"], "account")),
						("total_participants", Uint32(kwargs["total_participants"])),
						("ticket_price", Asset(kwargs["ticket_price"])),
						("latency_sec", Uint16(kwargs["latency_sec"])),
						("img_url", String(kwargs["img_url"])),
						("description", String(kwargs["description"]))
					]
				)
			)


class Lottery_goods_buy_ticket(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("lot_id", ObjectId(kwargs["lot_id"], "lottery_goods")),
						("participant", ObjectId(kwargs["participant"], "account")),
						("ticket_price", Asset(kwargs["ticket_price"]))
					]
				)
			)


class Lottery_goods_send_contacts(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]

			prefix = kwargs.get("prefix", default_prefix)
			if "winner_contacts" in kwargs and kwargs["winner_contacts"]:
				if isinstance(kwargs["winner_contacts"], dict):
					kwargs["winner_contacts"]["prefix"] = prefix
					winner_contacts = Memo(**kwargs["winner_contacts"])
				else:
					winner_contacts = Memo(kwargs["winner_contacts"])
			else:
				winner_contacts = None

			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("lot_id", ObjectId(kwargs["lot_id"], "lottery_goods")),
						("winner", ObjectId(kwargs["winner"], "account")),
						("winner_contacts", winner_contacts)
					]
				)
			)


class Lottery_goods_confirm_delivery(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("lot_id", ObjectId(kwargs["lot_id"], "lottery_goods")),
						("winner", ObjectId(kwargs["winner"], "account")),
					]
				)
			)


class Matrix_open_room(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("matrix_id", ObjectId(kwargs["matrix_id"], "matrix")),
						("player", ObjectId(kwargs["player"], "account")),
						("matrix_level", Uint8(kwargs["matrix_level"])),
						("level_price", Asset(kwargs["level_price"]))
					]
				)
			)

class Vesting_balance_create(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
		if kwargs["policy"][0] == 0:
			policy = Static_variant(
							Policy(begin_timestamp=kwargs["policy"][1]["begin_timestamp"], vesting_cliff_seconds=kwargs["policy"][1]["vesting_cliff_seconds"], vesting_duration_seconds=kwargs["policy"][1]["vesting_duration_seconds"]),
							 0)
		if kwargs["policy"][0] == 1:
			policy = Static_variant(
							Policy1(start_claim=kwargs["policy"][1]["start_claim"], vesting_seconds=kwargs["policy"][1]["vesting_seconds"]),
							 1)
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("creator", ObjectId(kwargs["creator"], "account")),
						("owner", ObjectId(kwargs["owner"], "account")),
						("amount", Asset(kwargs["amount"])),
						("policy", policy
						)
					]
				)
			)	



class Send_message(GrapheneObject):
	def __init__(self, *args, **kwargs):
		# Allow for overwrite of prefix
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			prefix = kwargs.get("prefix", default_prefix)
			if "memo" in kwargs and kwargs["memo"]:
				if isinstance(kwargs["memo"], dict):
					kwargs["memo"]["prefix"] = prefix
					memo = Memo(**kwargs["memo"])
				else:
					memo = Memo(kwargs["memo"])
			else:
				memo = None
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("from", ObjectId(kwargs["from"], "account")),
						("to", ObjectId(kwargs["to"], "account")),
						("memo", memo)
					]
				)
			)

class Resolve_p2p_dispute(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("p2p_order", ObjectId(kwargs["p2p_order"], "p2p_order")),
						("arbitr", ObjectId(kwargs["arbitr"], "account")),
						("winner", ObjectId(kwargs["winner"], "account")),
						("looser", ObjectId(kwargs["looser"], "account"))
					]
				)
			)

class Poc_vote(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("account", ObjectId(kwargs["account"], "account")),
						("poc3_vote", Asset(kwargs["poc3_vote"])),
						("poc6_vote", Asset(kwargs["poc6_vote"])),
						("poc12_vote", Asset(kwargs["poc12_vote"])),
					]
				)
			)

class Poc_stak(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("account", ObjectId(kwargs["account"], "account")),
						("stak_amount", Asset(kwargs["stak_amount"])),
						("staking_type", Uint8(kwargs["staking_type"])),
					]
				)
			)

class Mass_payment(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			
			payments = Map(
				[
					[ObjectId(e[0], "account"), Uint64(e[1])]
					for e in kwargs["payments"]
				]
			)
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("from", ObjectId(kwargs["from"], "account")),
						("asset_id", ObjectId(kwargs["asset_id"], "asset")),
						("payments", payments),
					]
				)
			)

class Approved_transfer_create(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("from",ObjectId(kwargs["from"], "account")),
						("to",ObjectId(kwargs["to"], "account")),
						("arbitr",ObjectId(kwargs["arbitr"], "account")),
						("expiration",PointInTime(kwargs["expiration"])),
						("amount",Asset(kwargs["amount"])),
					]
				)
			)

class Approved_transfer_approve(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("from",ObjectId(kwargs["from"], "account")),
						("to",ObjectId(kwargs["to"], "account")),
						("arbitr",ObjectId(kwargs["arbitr"], "account")),
						("amount",Asset(kwargs["amount"])),
						("ato",ObjectId(kwargs["ato"], "approved_transfer")),
					]
				)
			)

class Approved_transfer_open_dispute(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("from",ObjectId(kwargs["from"], "account")),
						("to",ObjectId(kwargs["to"], "account")),
						("arbitr",ObjectId(kwargs["arbitr"], "account")),
						("amount",Asset(kwargs["amount"])),
						("ato",ObjectId(kwargs["ato"], "approved_transfer")),
					]
				)
			)

class Approved_transfer_resolve_dispute(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("from",ObjectId(kwargs["from"], "account")),
						("to",ObjectId(kwargs["to"], "account")),
						("arbitr",ObjectId(kwargs["arbitr"], "account")),
						("amount",Asset(kwargs["amount"])),
						("winner",ObjectId(kwargs["winner"], "account")),
						("ato",ObjectId(kwargs["ato"], "approved_transfer")),
					]
				)
			)

class Edit_p2p_adv(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("p2p_adv", ObjectId(kwargs["p2p_adv"], "p2p_adv")),
						("p2p_gateway",ObjectId(kwargs["p2p_gateway"], "account")),
						("adv_type",Bool(bool(kwargs["adv_type"]))),
						("adv_description", String(str(kwargs["adv_description"]))),
						("max_cwd", Int64(int(kwargs["max_cwd"]))),
						("min_cwd", Int64(int(kwargs["min_cwd"]))),
						("price", Int64(int(kwargs["price"]))),
						("currency", String(str(kwargs["currency"]))),
						("min_p2p_complete_deals", Uint32(int(kwargs["min_p2p_complete_deals"]))),
						("min_account_status", Uint8(int(kwargs["min_account_status"]))),
						("timelimit_for_reply", Uint32(int(kwargs["timelimit_for_reply"]))),
						("timelimit_for_approve", Uint32(int(kwargs["timelimit_for_approve"]))),
						("geo", String(str(kwargs["geo"]))),
						("status", Uint8(int(kwargs["status"]))),
					]
				)
			)

# ================================================
class Account_transfer(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("account_id", ObjectId(kwargs["account_id"], "account")),
						("new_owner", ObjectId(kwargs["new_owner"], "account")),
						("extensions", Set([])),
					]
				)
			)
			
class Witness_create(GrapheneObject):
	def __init__(self, *args, **kwargs):
		prefix = kwargs.get("prefix", default_prefix)
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("witness_account", ObjectId(kwargs["witness_account"], "account")),
						("url", String(str(kwargs["url"]))),
						("block_signing_key", PublicKey(kwargs["block_signing_key"], prefix=prefix)),
					]
				)
			)
			
class Proposal_delete(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("fee_paying_account", ObjectId(kwargs["fee_paying_account"], "account")),
						("using_owner_authority", Bool(bool(kwargs["using_owner_authority"]))),
						("proposal", ObjectId(kwargs["proposal"], "proposal")),
						("extensions", Set([])),
					]
				)
			)
			
class Withdraw_permission_update(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("withdraw_from_account", ObjectId(kwargs["withdraw_from_account"], "account")),
						("authorized_account", ObjectId(kwargs["authorized_account"], "account")),
						("permission_to_update", ObjectId(kwargs["permission_to_update"], "withdraw_permission")),
						("withdrawal_limit", Asset(kwargs["withdrawal_limit"])),
						("withdrawal_period_sec", Uint32(int(kwargs["withdrawal_period_sec"]))),
						("period_start_time", PointInTime(kwargs["period_start_time"])),
						("periods_until_expiration", Uint32(int(kwargs["periods_until_expiration"]))),
					]
				)
			)
			
class Withdraw_permission_claim(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			prefix = kwargs.get("prefix", default_prefix)
			if "memo" in kwargs and kwargs["memo"]:
				if isinstance(kwargs["memo"], dict):
					kwargs["memo"]["prefix"] = prefix
					memo = Memo(**kwargs["memo"])
				else:
					memo = Memo(kwargs["memo"])
			else:
				memo = None
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("withdraw_permission", ObjectId(kwargs["withdraw_permission"], "withdraw_permission")),
						("withdraw_from_account", ObjectId(kwargs["withdraw_from_account"], "account")),
						("withdraw_to_account", ObjectId(kwargs["withdraw_to_account"], "account")),
						("amount_to_withdraw", Asset(kwargs["amount_to_withdraw"])),
						("memo", memo)
					]
				)
			)
			
class Withdraw_permission_delete(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("withdraw_from_account", ObjectId(kwargs["withdraw_from_account"], "account")),
						("authorized_account", ObjectId(kwargs["authorized_account"], "account")),
						("withdrawal_permission", ObjectId(kwargs["withdrawal_permission"], "withdraw_permission"))
					]
				)
			)
			
class Committee_member_update(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("committee_member", ObjectId(kwargs["committee_member"], "committee_member")),
						("committee_member_account", ObjectId(kwargs["committee_member_account"], "account")),
						("new_url", Optional(String(str(kwargs["new_url"]))))
					]
				)
			)

# NEED OBJECT!			
class Committee_member_update_global_parameters(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			super().__init__(
				OrderedDict(
					[

					]
				)
			)

# NEED OBJECT!
class Assert(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			super().__init__(
				OrderedDict(
					[

					]
				)
			)

# NEED OBJECT!			
class Transfer_to_blind(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			super().__init__(
				OrderedDict(
					[

					]
				)
			)

# NEED OBJECT!			
class Blind_transfer(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			super().__init__(
				OrderedDict(
					[

					]
				)
			)

# NEED OBJECT!			
class Transfer_from_blind(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			super().__init__(
				OrderedDict(
					[

					]
				)
			)
			
class Account_status_upgrade(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("account_to_upgrade", ObjectId(kwargs["account_to_upgrade"], "account")),
						("referral_status_type", Uint8(kwargs["referral_status_type"]))
					]
				)
			)
			
class Create_p2p_adv(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("p2p_gateway", ObjectId(kwargs["p2p_gateway"], "account")),
						("adv_type", Bool(bool(kwargs["adv_type"]))),
						("adv_description", String(str(kwargs["adv_description"]))),
						("max_cwd", Int64(int(kwargs["max_cwd"]))),
						("min_cwd", Int64(int(kwargs["min_cwd"]))),
						("price", Int64(int(kwargs["price"]))),
						("currency", String(str(kwargs["currency"]))),
						("min_p2p_complete_deals", Uint32(int(kwargs["min_p2p_complete_deals"]))),
						("min_account_status", Uint8(kwargs["min_account_status"])),
						("timelimit_for_reply", Uint32(int(kwargs["timelimit_for_reply"]))),
						("timelimit_for_approve", Uint32(int(kwargs["timelimit_for_approve"]))),
						("geo", String(str(kwargs["geo"]))),
					]
				)
			)
			
class Clear_p2p_adv_black_list(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("p2p_adv", ObjectId(kwargs["p2p_adv"], "p2p_adv")),
						("p2p_gateway", ObjectId(kwargs["p2p_gateway"], "account"))
					]
				)
			)
			
class Remove_from_p2p_adv_black_list(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("p2p_adv", ObjectId(kwargs["p2p_adv"], "p2p_adv")),
						("p2p_gateway", ObjectId(kwargs["p2p_gateway"], "account")),
						("blacklisted", ObjectId(kwargs["blacklisted"], "account"))
					]
				)
			)
			
class Create_p2p_order(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			prefix = kwargs.get("prefix", default_prefix)
			if "payment_details" in kwargs and kwargs["payment_details"]:
				if isinstance(kwargs["payment_details"], dict):
					kwargs["payment_details"]["prefix"] = prefix
					memo = Optional(Memo(**kwargs["payment_details"]))
				else:
					memo = Optional(Memo(kwargs["payment_details"]))
			else:
				memo = Optional(None)
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("p2p_adv", ObjectId(kwargs["p2p_adv"], "p2p_adv")),
						("amount", Asset(kwargs["amount"])),
						("price", Int64(int(kwargs["price"]))),
						("p2p_gateway", ObjectId(kwargs["p2p_gateway"], "account")),
						("p2p_client", ObjectId(kwargs["p2p_client"], "account")),
						("payment_details", memo)
					]
				)
			)
			
class Cancel_p2p_order(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("p2p_gateway", ObjectId(kwargs["p2p_gateway"], "account")),
						("p2p_client", ObjectId(kwargs["p2p_client"], "account")),
						("p2p_order", ObjectId(kwargs["p2p_order"], "p2p_order")),
						("blacklist", Bool(bool(kwargs["blacklist"])))
					]
				)
			)
			
class Call_p2p_order(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			prefix = kwargs.get("prefix", default_prefix)
			if "payment_details" in kwargs and kwargs["payment_details"]:
				if isinstance(kwargs["payment_details"], dict):
					kwargs["payment_details"]["prefix"] = prefix
					memo = Memo(**kwargs["payment_details"])
				else:
					memo = Memo(kwargs["payment_details"])
			else:
				memo = None
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("p2p_order", ObjectId(kwargs["p2p_order"], "p2p_order")),
						("p2p_gateway", ObjectId(kwargs["p2p_gateway"], "account")),
						("p2p_client", ObjectId(kwargs["p2p_client"], "account")),
						("amount", Asset(kwargs["amount"])),
						("price", Int64(int(kwargs["price"]))),
						("payment_details", memo)
					]
				)
			)
			
class Payment_p2p_order(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			prefix = kwargs.get("prefix", default_prefix)
			if "file_hash" in kwargs and kwargs["file_hash"]:
				if isinstance(kwargs["file_hash"], dict):
					kwargs["file_hash"]["prefix"] = prefix
					memo = Optional(Memo(**kwargs["file_hash"]))
				else:
					memo = Optional(Memo(kwargs["file_hash"]))
			else:
				memo = Optional(None)
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("p2p_order", ObjectId(kwargs["p2p_order"], "p2p_order")),
						("paying_account", ObjectId(kwargs["paying_account"], "account")),
						("recieving_account", ObjectId(kwargs["recieving_account"], "account")),
						("file_hash", memo)
					]
				)
			)
			
class Release_p2p_order(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("p2p_order", ObjectId(kwargs["p2p_order"], "p2p_order")),
						("paying_account", ObjectId(kwargs["paying_account"], "account")),
						("recieving_account", ObjectId(kwargs["recieving_account"], "account"))
					]
				)
			)
			
class Open_p2p_dispute(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			prefix = kwargs.get("prefix", default_prefix)
			if "contact_details" in kwargs and kwargs["contact_details"]:
				if isinstance(kwargs["contact_details"], dict):
					kwargs["contact_details"]["prefix"] = prefix
					memo = Memo(**kwargs["contact_details"])
				else:
					memo = Memo(kwargs["contact_details"])
			else:
				memo = None
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("p2p_order", ObjectId(kwargs["p2p_order"], "p2p_order")),
						("account", ObjectId(kwargs["account"], "account")),
						("defendant", ObjectId(kwargs["defendant"], "account")),
						("arbitr", ObjectId(kwargs["arbitr"], "account")),
						("contact_details", memo)
					]
				)
			)
			
class Reply_p2p_dispute(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			prefix = kwargs.get("prefix", default_prefix)
			if "contact_details" in kwargs and kwargs["contact_details"]:
				if isinstance(kwargs["contact_details"], dict):
					kwargs["contact_details"]["prefix"] = prefix
					memo = Memo(**kwargs["contact_details"])
				else:
					memo = Memo(kwargs["contact_details"])
			else:
				memo = None
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("p2p_order", ObjectId(kwargs["p2p_order"], "p2p_order")),
						("account", ObjectId(kwargs["account"], "account")),
						("arbitr", ObjectId(kwargs["arbitr"], "account")),
						("contact_details", memo)
					]
				)
			)
			
class Credit_system_get(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("debitor", ObjectId(kwargs["debitor"], "account")),
						("credit_amount", Asset(kwargs["credit_amount"]))
					]
				)
			)
			
class Credit_repay(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("debitor", ObjectId(kwargs["debitor"], "account")),
						("creditor", ObjectId(kwargs["creditor"], "account")),
						("repay_amount", Asset(kwargs["repay_amount"]))
					]
				)
			)
			
class Credit_offer_create(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("min_income", Int64(int(kwargs["min_income"]))),
						("creditor", ObjectId(kwargs["creditor"], "account")),
						("credit_amount", Asset(kwargs["credit_amount"])),
						("repay_amount", Asset(kwargs["repay_amount"]))
					]
				)
			)
			
class Credit_offer_cancel(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("creditor", ObjectId(kwargs["creditor"], "account")),
						("credit_offer", ObjectId(kwargs["credit_offer"], "credit_offer"))
					]
				)
			)
			
class Credit_offer_fill(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("debitor", ObjectId(kwargs["debitor"], "account")),
						("creditor", ObjectId(kwargs["creditor"], "account")),
						("credit_offer", ObjectId(kwargs["credit_offer"], "credit_offer")),
						("credit_amount", Asset(kwargs["credit_amount"]))
					]
				)
			)
			
class Pledge_offer_give_create(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("creditor", ObjectId(kwargs["creditor"], "account")),
						("pledge_amount", Asset(kwargs["pledge_amount"])),
						("credit_amount", Asset(kwargs["credit_amount"])),
						("repay_amount", Asset(kwargs["repay_amount"])),
						("pledge_days", Uint16(int(kwargs["pledge_days"])))
					]
				)
			)
			
class Pledge_offer_take_create(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("debitor", ObjectId(kwargs["debitor"], "account")),
						("pledge_amount", Asset(kwargs["pledge_amount"])),
						("credit_amount", Asset(kwargs["credit_amount"])),
						("repay_amount", Asset(kwargs["repay_amount"])),
						("pledge_days", Uint16(int(kwargs["pledge_days"])))
					]
				)
			)
			
class Pledge_offer_cancel(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("creator", ObjectId(kwargs["creator"], "account")),
						("pledge_offer", ObjectId(kwargs["pledge_offer"], "pledge_offer"))
					]
				)
			)
			
class Pledge_offer_fill(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("account", ObjectId(kwargs["account"], "account")),
						("debitor", ObjectId(kwargs["debitor"], "account")),
						("creditor", ObjectId(kwargs["creditor"], "account")),
						("pledge_amount", Asset(kwargs["pledge_amount"])),
						("credit_amount", Asset(kwargs["credit_amount"])),
						("repay_amount", Asset(kwargs["repay_amount"])),
						("pledge_days", Uint16(int(kwargs["pledge_days"]))),
						("pledge_offer", ObjectId(kwargs["pledge_offer"], "pledge_offer"))
					]
				)
			)
			
class Pledge_offer_repay(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("debitor", ObjectId(kwargs["debitor"], "account")),
						("creditor", ObjectId(kwargs["creditor"], "account")),
						("repay_amount", Asset(kwargs["repay_amount"])),
						("pledge_amount", Asset(kwargs["pledge_amount"])),
						("pledge_offer", ObjectId(kwargs["pledge_offer"], "pledge_offer"))
					]
				)
			)
			
class Committee_member_update_gamezone_parameters(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			super().__init__(
				OrderedDict(
					[

					]
				)
			)
			
class Committee_member_update_staking_parameters(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			super().__init__(
				OrderedDict(
					[

					]
				)
			)
			
class Exchange_silver(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("account", ObjectId(kwargs["account"], "account")),
						("amount", Asset(kwargs["amount"] ))
					]
				)
			)
			
class Buy_gcwd(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("account", ObjectId(kwargs["account"], "account")),
						("amount", Asset(kwargs["amount"] ))
					]
				)
			)
			
class Change_referrer(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("account_id", ObjectId(kwargs["account_id"], "account")),
						("new_referrer", ObjectId(kwargs["new_referrer"], "account"))
					]
				)
			)
			
class Gr_team_create(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("captain", ObjectId(kwargs["captain"], "account")),
						("name", String(str(kwargs["name"]))),
						("description", String(str(kwargs["description"]))),
						("logo", String(str(kwargs["logo"]))),
					]
				)
			)
			
class Gr_team_delete(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("captain", ObjectId(kwargs["captain"], "account")),
						("team", ObjectId(kwargs["team"], "gr_team"))
					]
				)
			)
			
class Gr_invite_send(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("captain", ObjectId(kwargs["captain"], "account")),
						("player", ObjectId(kwargs["player"], "account")),
						("team", ObjectId(kwargs["team"], "gr_team"))
					]
				)
			)
			
class Gr_invite_accept(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("captain", ObjectId(kwargs["captain"], "account")),
						("player", ObjectId(kwargs["player"], "account")),
						("team", ObjectId(kwargs["team"], "gr_team")),
						("invite", ObjectId(kwargs["invite"], "gr_invite"))
					]
				)
			)
			
class Gr_player_remove(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("captain", ObjectId(kwargs["captain"], "account")),
						("player", ObjectId(kwargs["player"], "account")),
						("team", ObjectId(kwargs["team"], "gr_team"))
					]
				)
			)
			
class Gr_team_leave(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("captain", ObjectId(kwargs["captain"], "account")),
						("player", ObjectId(kwargs["player"], "account")),
						("team", ObjectId(kwargs["team"], "gr_team"))
					]
				)
			)
			
class Gr_vote(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("player", ObjectId(kwargs["player"], "account")),
						("gr_iron_volume", Int64(int(kwargs["gr_iron_volume"]))),
						("gr_bronze_volume", Int64(int(kwargs["gr_bronze_volume"]))),
						("gr_silver_volume", Int64(int(kwargs["gr_silver_volume"]))),
						("gr_gold_volume", Int64(int(kwargs["gr_gold_volume"]))),
						("gr_platinum_volume", Int64(int(kwargs["gr_platinum_volume"]))),
						("gr_diamond_volume", Int64(int(kwargs["gr_diamond_volume"]))),
						("gr_master_volume", Int64(int(kwargs["gr_master_volume"]))),
						("gr_iron_reward", Int64(int(kwargs["gr_iron_reward"]))),
						("gr_bronze_reward", Int64(int(kwargs["gr_bronze_reward"]))),
						("gr_silver_reward", Int64(int(kwargs["gr_silver_reward"]))),
						("gr_gold_reward", Int64(int(kwargs["gr_gold_reward"]))),
						("gr_platinum_reward", Int64(int(kwargs["gr_platinum_reward"]))),
						("gr_diamond_reward", Int64(int(kwargs["gr_diamond_reward"]))),
						("gr_elite_reward", Int64(int(kwargs["gr_elite_reward"]))),
						("gr_master_reward", Int64(int(kwargs["gr_master_reward"])))
					]
				)
			)
			
class Gr_range_bet(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("team", ObjectId(kwargs["team"], "gr_team")),
						("lower_rank", Uint8(kwargs["lower_rank"])),
						("upper_rank", Uint8(kwargs["upper_rank"])),
						("result", Bool(bool(kwargs["result"]))),
						("bettor", ObjectId(kwargs["bettor"], "account")),
						("bet", Asset(kwargs["bet"] ))
					]
				)
			)
			
class Gr_team_bet(GrapheneObject):
	def __init__(self, *args, **kwargs):
		if isArgsThisClass(self, args):
			self.data = args[0].data
		else:
			if len(args) == 1 and len(kwargs) == 0:
				kwargs = args[0]
			super().__init__(
				OrderedDict(
					[
						("fee", Asset(kwargs["fee"])),
						("team1", ObjectId(kwargs["team1"], "gr_team")),
						("team2", ObjectId(kwargs["team2"], "gr_team")),
						("winner", ObjectId(kwargs["winner"], "gr_team")),
						("bettor", ObjectId(kwargs["bettor"], "account")),
						("bet", Asset(kwargs["bet"] ))
					]
				)
			)

fill_classmaps()